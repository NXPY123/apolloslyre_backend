from flask import Blueprint, request, jsonify, current_app, Flask

from werkzeug.utils import secure_filename
import os
import uuid
from flask_cors import CORS
from .db import get_db

from .tasks import extract_epub

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'epub'}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file_with_unique_id(file):
    '''
    Generate a unique id for the file and save it to the UPLOAD_FOLDER
    '''
    unique_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    unique_filename = f"{unique_id}_{filename}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    return unique_filename, file_path

@main.route('/upload', methods=['POST'])
def upload_file():


    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):

        unique_filename, file_path = save_file_with_unique_id(file)
        print(unique_filename, file_path)
        # Store the file_path in the database
        db = get_db()
        # STore unique_filename and file_path in the database
        db.execute('INSERT INTO files (unique_filename, file_path) VALUES (?, ?)', (unique_filename, file_path))
        db.commit()
        print("ADSS")
        # Send the file_path to the task queue. Get the id of the task
        task = extract_epub.delay(file_path, unique_filename)
        task_id = task.id

        return jsonify({'task_id': task_id,
                        "unique_filename": unique_filename,
                        }), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400
    

# Endpoint to get the status of the task
@main.route('/status', methods=['GET'])
def task_status():
    task_id = request.args.get('task_id')
    task = extract_epub.AsyncResult(task_id)
    response = {
        'state': task.state,
        'task_id': task_id
    }
    return jsonify(response), 200

# Endpoint to get the processed file
@main.route('/processed', methods=['GET'])
def processed_file():
    unique_filename = request.args.get('unique_filename')
    file_path = os.path.join(current_app.config['PROCESSED_FOLDER'], unique_filename)
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            content = file.read()
        return jsonify({'content': content}), 200
    else:
        return jsonify({'error': 'File not found'}), 404
