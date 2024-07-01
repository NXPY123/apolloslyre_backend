from celery import shared_task
from  epubExtractionPackage_NY import epubextract
from flask import current_app
import os
import json

playlists = {
    "adventure": "spotify:playlist:6V1mIajl4J77udiRzSKW9n?si=5b293dee45114d7b",
    "electronic": "spotify:playlist:4QPYGjdwji1ZrhyVRhJzc4?si=5f525fc486fa4f82",
    "acoustic": "spotify:playlist:18zwlTqUMXYPGRrN439zvj?si=4e03623b11d14579",
    "ambient": "spotify:playlist:7Dn4Eh8ZxGdjxC2ngH1PEY?si=1d9ec6dd465e4edc",
    "classical": "spotify:playlist:4p3D834U8NjfUozgjjRZmc?si=65c3f11053ab4161",
    "jazz": "spotify:playlist:2bBmk8ayezfqmlhGWAxVZj?si=fc38e3258c7640bf",
    "cinematic": "spotify:playlist:7e49PXK5nz9JbAcPFbrFhL?si=c355ef69b5aa4ddb",
    "horror": "spotify:playlist:0rI7IC9OtdTeWwYFwy4m81?si=8383aebb20894c22",
    "romantic": "spotify:playlist:2XGqjaldJQSrYsCZSTtEjh?si=fcd62e678c9a491b",
    "mystery": "spotify:playlist:6tJo2efccNrNpElJ24llC2?si=654eeec3e05c4e9a"
}

@shared_task
def extract_epub(epub_path,unique_filename):


    # Extract the epub
    extractor = epubextract.EpubExtractorFactory.get_extractor(epub_path)
    content = extractor.extract_content()

    # Send a request to the API
    # API Logic here

    # Assume we get a list of tuples [(chapter_title, mood)]

    chapter_mood = [(f"Chapter {i}", "adventure") for i in range(1, 10)]
    chapter_playlists = {}

    for chapter, mood in chapter_mood:
        # Retrieve playlist url for each mood
        # Playlist Logic here
       
        playlist_url = playlists[mood.lower()]

        chapter_playlists[chapter] = playlist_url

    # Convert to JSON and store as file in instance/processed with the filename as the unique_filename.json
    filename = unique_filename.split(".")[0]
    filename = filename + ".json"
    json_content = json.dumps(chapter_playlists)
    filename = os.path.join(current_app.config["PROCESSED_FOLDER"],unique_filename)
    with open(file=filename,mode="w") as file:
        file.write(json_content)
    
    return filename
    
    

    


    




        
        
        
