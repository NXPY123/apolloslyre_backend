# Setting up the Backend with Docker Compose
Step 1: Clone the repo
```bash
git clone https://github.com/NXPY123/apolloslyre_backend.git
```

Step 2: Add the model to the Serving/Model directory
```bash
cd apolloslyre_backend/Serving/Model
mkdir big-bird
cd big-bird
// Add the model files in the big-bird directory
```

Step 3: Generate the .mar file
```bash
cd apolloslyre_backend/Serving/Model
torch-model-archiver \
    --model-name bigbird \
    --version 1.0 \
    --serialized-file big-bird/model.safetensors \
    --extra-files "big-bird/tokenizer_config.json,big-bird/special_tokens_map.json,big-bird/config.json,big-bird/spiece.model,bigbird_handler.py" \
    --handler bigbird_handler.py \
    --export-path ./model-store
```

Step 4: Build the docker images
```bash
cd apolloslyre_backend
docker-compose build
```

Step 5: Start the docker containers
```bash
docker-compose up
```

Step 6: Test the server
```bash
curl -X POST -F "file=@/path/to/epub/file.epub" http://localhost:8001/upload
curl -X GET "http://localhost:8001/status?task_id=task_id_returned_from_previous_request"
curl -X GET "http://localhost:8001/processed?unique_filename=unique_filename_returned_from_first_request"
```


# Setting up the Backend without Docker Compose

## Starting the Backend

Step 1: Clone the repo
```bash
git clone https://github.com/NXPY123/apolloslyre_backend.git
```

Step 2: Create a virtual environment and install dependencies
```bash
cd apolloslyre_backend
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --index-url https://test.pypi.org/simple/ --no-deps epubExtractionPackage-NY --upgrade
```

Step 3: Put the model in the instance directory
```bash
mkdir instance
cd instance
mkdir big-bird
// Add the model files in the big-bird directory
cd ..
```

Step 4: Initialize and create the database
```bash
export FLASK_APP=flaskr FLASK_ENV=development 
python -m flask init-db            
```

Step 5: Start redis server on port 6379

Step 6: Start the celery worker
```bash
python -m celery -A make_celery worker -P threads --loglevel=info 
```

Step 7: Set instance path
```bash
export FLASK_INSTANCE_PATH=/path/to/instance
``` 

Step 8: Start the flask server
```bash
python -m flask run --debug --host=0.0.0.0 --port=8000  
```

## Starting the Inference Server

Step 1: Clone the repo if not already done
```bash
git clone https://github.com/NXPY123/apolloslyre_backend.git
```

Step 2: Create a virtual environment and install dependencies if not already done
```bash
cd apolloslyre_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install --index-url https://test.pypi.org/simple/ --no-deps epubExtractionPackage-NY --upgrade
```

Step 3: Put the model in the Serving/Model directory with the directory name "big-bird"
```bash
cd Serving/Model
mkdir big-bird
cd big-bird
// Add the model files in the big-bird directory
```
The following files should be present in the big-bird directory:
1. config.json
2. model.safetensors
3. special_tokens_map.json
4. spiece.model
5. tokenizer_config.json

Step 4: Generate the .mar file
```bash
cd Serving/Model

torch-model-archiver \
    --model-name bigbird \
    --version 1.0 \
    --serialized-file big-bird/model.safetensors \
    --extra-files "big-bird/tokenizer_config.json,big-bird/special_tokens_map.json,big-bird/config.json,big-bird/spiece.model,big-bird_handler.py" \
    --handler big-bird_handler.py \
    --export-path model_store
```

Step 5: Test the bigbird_handler.py file on the model
```bash
cd Serving/Model/tests
python handler_test.py
```

Step 6: Build the docker image
```bash
cd Serving
docker build -t bigbird-torchserve .
```

Step 7: Run the docker image
```bash
 docker run -d -p 8080:8080 -p 8081:8081 --memory=8g --cpus=4 --name bigbird-server bigbird-torchserve
```

Step 8: Test the server
```bash
curl -X POST http://127.0.0.1:8080/predictions/bigbird \
    -H "Content-Type: application/json" \
    -d '[
        ["Chapter 1", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."],
        ["Chapter 2", "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."],
        ["Chapter 3", "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."],
        ["Chapter 4", "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."]
    ]'

```




