# Dockerfile for dev environment into a VPS

# Use the official Python base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file to the working directory
COPY ./tractors-be/requirements.txt /code/

# Volume with brands (TEMP FOR VPS)
VOLUME ["/code/static/uploads"]

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code to the working directory
COPY ./tractors-be/ /code/

# Expose the port on which your Django application will run
EXPOSE 8000

# Run the Django application
CMD ["sh", "-c", "chmod +x ./run.sh && ./run.sh"]