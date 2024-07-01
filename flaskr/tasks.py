from celery import shared_task
from  epubExtractionPackage_NY import epubextract
from flask import current_app
import os
import json

@shared_task
def extract_epub(epub_path,unique_filename):

    # Get file 
    with open(epub_path, 'rb') as file:
        epub_file = file.read()

    # Extract the epub
    extractor = epubextract.EpubExtractorFactory.get_extractor(file)
    content = extractor.extract_content()

    # Send a request to the API
    # API Logic here

    # Assume we get a list of tuples [(chapter_title, mood)]

    chapter_mood = [(f"Chapter {i}", "Happy") for i in range(1, 10)]
    chapter_playlists = {}

    for chapter, mood in chapter_mood:
        # Retrieve playlist url for each mood
        # Playlist Logic here
        playlists = {
            "happy": "https://www.youtube.com/watch?v=6Dh-RL__uN4",
        }

        playlist_url = playlists[mood.lower()]

        chapter_playlists[chapter] = playlist_url

    # Convert to JSON and store as file in instance/processed with the filename as the unique_filename.json
    filename = unique_filename.split(".")[0]
    filename = filename + ".json"
    json_content = json.dumps(chapter_playlists)
    filename = os.path.join(current_app.config["PROCESSED_FOLDER"],unique_filename)
    with open(file=filename,mode="w") as file:
        file.write(json_content)

    


    




        
        
        
