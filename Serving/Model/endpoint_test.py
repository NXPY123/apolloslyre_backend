import  requests
import json


def send_api_request(data):

    url = "http://localhost:8080/predictions/bigbird"
    # Comvert list of tuples to list of lists
    request_data = [[chapter, text] for chapter, text in data]
    response = requests.post(
        url, 
        headers={"Content-Type": "application/json"}, 
        json=request_data  # Convert Python list to JSON
    )

    print(response.json())

send_api_request([("Chapter1", "Your input text goes here."), ("Chapter2", "Another input text.")])


