To get the backend running:

Step 1: Clone the repo
```bash
git clone https://github.com/NXPY123/apolloslyre_backend.git
```

Step 2: Create a virtual environment and install dependencies
```bash
cd apolloslyre_backend
python3 -m venv venv
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
flask --app flaskr init-db
```

Step 5: Start redis server on port 6379

Step 6: Start the celery worker
```bash
celery -A make_celery worker -P threads --loglevel=info 
```

Step 7: Start the flask server
```bash
flask --app flaskr run --debug
```


