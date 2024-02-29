# DEV.Dockerfile for development environment

# Python version to use
FROM python:3.11

# Working directory
WORKDIR /tractors/tractors-be

# Copy requirements.txt to working directory
COPY requirements.txt .
RUN pip install -r requirements.txt

# Port to expose
EXPOSE 8000

# Create volume of current directory
VOLUME ["/tractors/tractors-be"]