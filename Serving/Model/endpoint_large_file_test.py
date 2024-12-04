import  requests
import json
from  epubExtractionPackage_NY import epubextract


def send_api_request(data):

    url = "http://localhost:8080/predictions/bigbird"
    # Comvert list of tuples to list of lists
    request_data = [{"data": text.decode("utf-8") if isinstance(text, bytes) else text, "chapter": chapter.decode("utf-8") if isinstance(chapter, bytes) else chapter} for chapter, text in data]
    for request in request_data:
        response = requests.post(
            url, 
            headers={"Content-Type": "application/json"}, 
            data=json.dumps([request])
        )
        print(response.json())
    

    return response.json()


file_path = "/Users/neeraj_py/Downloads/20211228.epub"
extractor = epubextract.EpubExtractorFactory.get_extractor(file_path)
content = extractor.extract_content()

print("Extracted content")
# Send a request to the API
response = send_api_request(content)
print("Predicted moods")
print(response)




