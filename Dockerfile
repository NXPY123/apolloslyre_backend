# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install the epubExtractionPackage-NY from TestPyPI
RUN pip install --index-url https://test.pypi.org/simple/ --no-deps epubExtractionPackage-NY --upgrade

# Copy the current directory contents into the container at /app
COPY . .

# Create the instance, uploads, and processed folders
RUN mkdir -p /app/instance/uploads
RUN mkdir -p /app/instance/processed

# Run the application
#CMD ["flask", "--app", "flaskr", "init-db", "&&", "flask", "run", "--host=0.0.0.0", "--port=8000"]

# Expose the port for Flask
EXPOSE 8000
