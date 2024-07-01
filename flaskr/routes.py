from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from .db import get_db


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
        # Store the file_path in the database
        db = get_db()
        # STore unique_filename and file_path in the database
        db.execute('INSERT INTO files (unique_filename, file_path) VALUES (?, ?)', (unique_filename, file_path))
        db.commit()
        
        '''
         [Logic to process the file here] 
        '''

        # Return a response with the unique_filename
        return jsonify({'unique_filename': unique_filename}), 201

    else:
        return jsonify({'error': 'File type not allowed'}), 400