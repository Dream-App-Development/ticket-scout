# Use the public ECR image for AWS Lambda with Python 3.10
FROM public.ecr.aws/lambda/python:3.10

# Set environment variables to prevent Python from writing pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the requirements file into the container
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app ${LAMBDA_TASK_ROOT}/app

# Command to run the Lambda function
CMD ["app.app.lambda_handler"]


# The code below for running in local machine
#
## Use the official Python image from the Docker Hub
#FROM python:3.10-slim

## Set environment variables to prevent Python from writing pyc files and buffering stdout and stderr
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
## Set the working directory in the container
#WORKDIR /app
#
## Copy the requirements file into the container
#COPY requirements.txt .
#
## Install the dependencies
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copy the application code into the container
#COPY . .
#
## Expose the port the app runs on
#EXPOSE 8000
#
## Define the command to run the application
#CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
