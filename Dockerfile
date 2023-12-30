# Use the official Python image as a base image
FROM python:3.12

# # Set environment variables
# ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container at /app
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app /app/

# Command to run the application
CMD ["python", "main.py", "--host", "127.0.0.1", "--port", "8000"]
