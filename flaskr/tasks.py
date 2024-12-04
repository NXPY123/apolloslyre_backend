from celery import shared_task
from  epubExtractionPackage_NY import epubextract
from flask import current_app
import os
import json
import torch
import requests


playlists = {
    "adventure": "spotify:playlist:6V1mIajl4J77udiRzSKW9n?si=5b293dee45114d7b",
    "electronic": "spotify:playlist:4QPYGjdwji1ZrhyVRhJzc4?si=5f525fc486fa4f82",
    "acoustic/folk": "spotify:playlist:18zwlTqUMXYPGRrN439zvj?si=4e03623b11d14579",
    "ambient": "spotify:playlist:7Dn4Eh8ZxGdjxC2ngH1PEY?si=1d9ec6dd465e4edc",
    "classical": "spotify:playlist:4p3D834U8NjfUozgjjRZmc?si=65c3f11053ab4161",
    "jazz": "spotify:playlist:2bBmk8ayezfqmlhGWAxVZj?si=fc38e3258c7640bf",
    "cinematic": "spotify:playlist:7e49PXK5nz9JbAcPFbrFhL?si=c355ef69b5aa4ddb",
    "horror": "spotify:playlist:0rI7IC9OtdTeWwYFwy4m81?si=8383aebb20894c22",
    "romantic": "spotify:playlist:2XGqjaldJQSrYsCZSTtEjh?si=fcd62e678c9a491b",
    "mystery/noir": "spotify:playlist:6tJo2efccNrNpElJ24llC2?si=654eeec3e05c4e9a"
}


label_to_genre = {0: 'Electronic', 1: 'Adventure', 2: 'Mystery/Noir', 3: 'Classical', 4: 'Cinematic', 5: 'Horror', 6: 'Romantic', 7: 'Acoustic/Folk', 8: 'Ambient'}


def send_api_request(data):

    # Check environment variable to determine if we are in development or production
    # If in development, use the local API
    # If in production, use the deployed API
    if os.getenv("FLASK_ENV") == "development":
        url = "http://localhost:8080/predictions/bigbird"
    elif os.getenv("FLASK_ENV") == "production":
        url = "http://torchserve:8080/predictions/bigbird"
    else:
        raise Exception("Environment not set. Please set the FLASK_ENV environment variable to either development or production.")
    
    # Convert list of tuples to list of lists
    request_data = [{"data": text.decode("utf-8") if isinstance(text, bytes) else text, "chapter": chapter.decode("utf-8") if isinstance(chapter, bytes) else chapter} for chapter, text in data]
    # Print the first key value pair
    responses = []
    for request in request_data:
        response = requests.post(
            url, 
            headers={"Content-Type": "application/json"}, 
            data=json.dumps([request])
        )
        responses.append(response.json()[0])

    return responses




@shared_task
def extract_epub(epub_path,unique_filename):

    print("Extracting epub")
    # Extract the epub
    extractor = epubextract.EpubExtractorFactory.get_extractor(epub_path)
    content = extractor.extract_content()

    print("Extracted content")
    # Send a request to the API
    # API Logic here

    if content is None:
        raise Exception("An error occured while extracting the content of the epub file. Please check the file and try again.")
    

    # Pass the list of tuples as a list of dictionary to the inference server via the API
    predictions = send_api_request(content)
    print("Predicted moods")

    print(predictions)
    chapter_playlists = {}
    
    for prediction in predictions:
        # Retrieve playlist url for each mood
        # Playlist Logic here
        chapter = list(prediction.keys())[0]
        mood = label_to_genre[prediction[chapter]]
       
        playlist_url = playlists[mood.lower()]

        chapter_playlists[chapter] = playlist_url
    
    print("Generated playlists")

    # Convert to JSON and store as file in instance/processed with the filename as the unique_filename.json
    filename = unique_filename.split(".")[0]
    filename = filename + ".json"
    json_content = json.dumps(chapter_playlists)
    filename = os.path.join(current_app.config["PROCESSED_FOLDER"],unique_filename)
    with open(file=filename,mode="w") as file:
        file.write(json_content)
    
    return filename
    
    

    


    




        
        
        
