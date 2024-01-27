#!/bin/bash

echo "Building Docker image for paperless-ngx-openai-title..."
docker build -t paperless-ngx-openai-title:latest .

# Start the docker-compose services
echo "Starting services with docker-compose..."
docker-compose up --detach

echo "Re-attaching to console logs"
docker-compose logs -f
echo "Service are up and running."
