import  requests
import json


def send_api_request(data):

    url = "http://localhost:8080/predictions/bigbird"
    # Comvert list of tuples to list of lists
    #request_data = [[chapter, text] for chapter, text in data]
    response = requests.post(
        url, 
        headers={"Content-Type": "application/json"}, 
        data=json.dumps(data)
    )

    return response.json()

response = send_api_request([{'data': 'Love Happiness Joy Friendship', "chapter": "Chapter1"}, {'data': 'Dangerous, scary, bloody, gore.', "chapter": "Chapter2"}])
print(response)



