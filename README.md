# Overview

This project is build using FastAPI. This exposes APIs for generating content from text files. This project can be easily deployed using docker containers. 

# Project-Setup

### Requirements : docker , docker-compose v2.23.3

* ### Clone git repo

> git clone https://github.com/xeroxPanda32/ByteGenieBackend.git

* ### Create S3 Bucket on AWS

* ### Create IAM user with persmission to access S3 Bucket created above.

* ### Add Environment files

add **.env** file in root directory

> **MONGO_URI**=mongo_connection_string

> **AWSAccessKeyId**=aws_access_key_id

> **AWSSecretKey**=aws_secret_access_key

> **AWS_REGION**=aws_region

> **AWS_BUCKET_NAME**=aws_bucket_name

<br>
public url of google colab where ML code is running

> **ML_URL**=https://646f-34-90-50-191.ngrok-free.app

* ### build & run docker container

inside root folder

> sudo docker-compose up

This should build and run the docker container at port 8000.

# Data Pre-processing

Ensure that the .txt file uploaded is descriptive in nature. Avoid urls, images and numbers.

# API

* uploadfile : API to generate content from ML

    > end point: "/getdoc/uploadfile"

    > method: POST

    > parameters: form-date { "file" : .txt file} 

    > return : JSON {
                "user_id": "user_id",
                "request_id": "_id",
                "prompt": "text extracted from file",
                "ml_response": "content_received_from_ml",
                "isSuccess": True
            }


* responsedetails: API to get detailed ML response stored in database

    > end point: backenedUrl + "/getdoc/responsedetails"
    
    > method: GET

    > parameters:  { params: { id }}

    > return : { _id, user_id, request_id, prompt: "a girl and a boy led to .", ml_response: { modelResponse : "a girl and a boy led to ...", isSuccess: true } }

* allResponses: API to get all previosly generated ML content

    > end point: backenedUrl+'/getdoc/allResponses'

    > method: GET

    > parameters: None

    > return : [ { _id, user_id, request_id, prompt: "a girl and a boy led to .", ml_response: { modelResponse : "a girl and a boy led to ...", isSuccess: true }}]


# Key Challenges

   > Previously worked on Nodejs , so working on FastAPI was a bit challenging in the start. 

   > Faced problem in setting up docker 

   > Faced problem in deploying the app on AWS server. Initially hosted the docker image on ECR and deployed the container on ECS. But ECS provided http communication whereas frontend was deployed on Amplify (https). Solved this by moving both frontend and backend to EC2 for better management. 
# Improvements

* User Authentication

    > Implement user authentication system

* Rate limiter, load balancer, 

    > Implement rate limiter

    > Implement load balancer

    > Setup CI/CD

    > Fine tuning ML Model