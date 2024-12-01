# Starting the Backend

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
flask --app flaskr run --debug
```

# Starting the Inference Server

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
docker run -d -p 8080:8080 -p 8081:8081 --name bigbird-server bigbird-torchserve
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




