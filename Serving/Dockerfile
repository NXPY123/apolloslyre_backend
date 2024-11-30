# Use the official PyTorch Serve image as the base
FROM pytorch/torchserve:latest-cpu

# Set the working directory inside the container
WORKDIR /home/model-server

RUN pip install --no-cache-dir transformers==4.42.3 sentencepiece

# Copy the model archive and handler to the container
COPY ./Model/model-store /home/model-server/model-store/
COPY config.properties /home/model-server/

# Expose the ports for TorchServe
EXPOSE 8080 8081

# Start the TorchServe server
CMD ["torchserve", "--start","--disable-token-auth", "--model-store", "/home/model-server/model-store", "--ts-config", "/home/model-server/config.properties"]
