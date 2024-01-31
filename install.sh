#!/bin/bash

# Define a name for your Docker image
IMAGE_NAME="paperless-ngx-openai-title"

# Build the Docker image
echo "Building Docker image for paperless-ngx-openai-title..."
docker build -t $IMAGE_NAME .

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Docker image built successfully."

    # Run docker-compose
    echo "Starting Docker Compose..."
    docker-compose up -d

    if [ $? -eq 0 ]; then
        echo "Docker Compose started successfully."
        echo "Displaying Docker Compose logs..."
        
        # Display Docker Compose logs
        docker-compose logs -f
    else
        echo "Error starting Docker Compose."
    fi
else
    echo "Error building Docker image."
fi