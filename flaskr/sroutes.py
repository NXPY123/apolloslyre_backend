#this is a temporary file it uses ebooklib and beatiful soup to extract text and i have used placeholder for the model
#still have to check the working of this code
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from .db import get_db
from ebooklib import epub
from bs4 import BeautifulSoup

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'epub'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file_with_unique_id(file):
    unique_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    unique_filename = f"{unique_id}_{filename}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    return unique_filename, file_path

def extract_chapters_from_epub(file_path):
    book = epub.read_epub(file_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            chapter_text = soup.get_text()
            chapters.append(chapter_text)
    return chapters

def classify_text(text):
    #default function placeholder for the model
    genres = ["Classical", "Ambient", "Jazz", "Electronic", "Cinematic", "Acoustic/Folk", "Horror", "Romantic", "Adventure", "Mystery/Noir"]
    import random
    return random.choice(genres)

GENRE_TO_SPOTIFY_PLAYLIST = {
    "Adventure": "spotify:playlist:6V1mIajl4J77udiRzSKW9n?si=5b293dee45114d7b",
    "Electronic": "spotify:playlist:4QPYGjdwji1ZrhyVRhJzc4?si=5f525fc486fa4f82",
    "Acoustic": "spotify:playlist:18zwlTqUMXYPGRrN439zvj?si=4e03623b11d14579",
    "Ambient": "spotify:playlist:7Dn4Eh8ZxGdjxC2ngH1PEY?si=1d9ec6dd465e4edc",
    "Classical": "spotify:playlist:4p3D834U8NjfUozgjjRZmc?si=65c3f11053ab4161"
    "Jazz": "spotify:playlist:2bBmk8ayezfqmlhGWAxVZj?si=fc38e3258c7640bf",
    "Cinematic": "spotify:playlist:7e49PXK5nz9JbAcPFbrFhL?si=c355ef69b5aa4ddb",
    "Horror": "spotify:playlist:0rI7IC9OtdTeWwYFwy4m81?si=8383aebb20894c22",
    "Romantic": "spotify:playlist:2XGqjaldJQSrYsCZSTtEjh?si=fcd62e678c9a491b",
    "Mystery": "spotify:playlist:6tJo2efccNrNpElJ24llC2?si=654eeec3e05c4e9a"
}

def genre_to_spotify_playlist(genre):
    return GENRE_TO_SPOTIFY_PLAYLIST.get(genre, "spotify:playlist:7e49PXK5nz9JbAcPFbrFhL?si=c355ef69b5aa4ddb")

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        unique_filename, file_path = save_file_with_unique_id(file)
        
        # Extract chapters from the EPUB file
        chapters = extract_chapters_from_epub(file_path)
        
        # Initialize the database connection
        db = get_db()
        
        chapter_genres = []
        for i, chapter_text in enumerate(chapters):
            # Classify the chapter text
            genre = classify_text(chapter_text)
            chapter_genres.append((i + 1, genre))
            
            # Store the chapter and genre in the database
            db.execute('INSERT INTO chapters (file_id, chapter_number, text, genre) VALUES (?, ?, ?, ?)', 
                       (unique_filename, i + 1, chapter_text, genre))
        
        db.commit()

        # Map genres to Spotify playlists
        playlists = {genre: genre_to_spotify_playlist(genre) for _, genre in chapter_genres}
        
        # Return the chapter-wise genres and playlist URLs
        return jsonify({'unique_filename': unique_filename, 'chapter_genres': chapter_genres, 'playlists': playlists}), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400
