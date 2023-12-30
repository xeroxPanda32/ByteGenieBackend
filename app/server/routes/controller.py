from fastapi import APIRouter, Body, UploadFile, File, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from botocore.exceptions import ClientError
from datetime import datetime
import boto3
import httpx

from server.database import (
    add_user,
    add_request,
    add_response,
    get_response,
)

from server.model.schema import (
    UserSchema,
    RequestSchema,
    ResponseSchema,
)

from server.config.config import (
    ML_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION_NAME,
    AWS_BUCKET_NAME
)

router = APIRouter()

# s3 configuration
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

# function to upload file on s3
def upload_to_s3(file, object_name):
    try:
        s3_client.upload_fileobj(file, AWS_BUCKET_NAME, object_name)
           # Construct the S3 URL
        s3_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{object_name}"
        return s3_url
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {e}")
    
async def read_file_s3(s3_file_key: str):
    try:
         response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=s3_file_key)
         text_content = response['Body'].read().decode('utf-8')
         return text_content
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to read the file: {e}")
   

async def sending_ml(dataSent: dict = Body(...)):
    sendingdoc = {"prompt" : dataSent}
    url = str(ML_URL+"/generateContent")
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, json=sendingdoc, timeout=50)
           # Check if the request was successful (status code 200)
            response.raise_for_status()
            result = response.json()
        return result

    except httpx.HTTPStatusError as e:
        print(e.response)
        # Handle HTTP status errors
        raise HTTPException(status_code=e.response.status_code, detail=f"Request to other server failed with status code {e.response.status_code}")

    except httpx.ReadTimeout as e:
        # Handle read timeout errors
        raise HTTPException(status_code=408, detail=f"Request to other server timed out: {str(e)}")

    except httpx.RequestError as e:
        # Handle other request errors (e.g., network issues)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

async def responseDetail(id: str):
    response = await get_response(id)
    response["_id"] = str(response["_id"])
    return response


async def upload_file_generate_response(file: UploadFile = File(...)):
    file_extension = file.filename.split('.')
    object_name = file_extension[0] +'_' + str(datetime.timestamp(datetime.now())) + '.' + file_extension[-1]
    s3_url =  upload_to_s3(file.file, object_name)
    doc_request = {
         "user_id": "6584783234d002610b9db873",
                "doc_url": str(s3_url),
                "doc_name":  str(object_name),
                "is_valid": True,
                "timestamp": datetime.now().isoformat()

    }
    doc_request["timestamp"] = str(doc_request["timestamp"])
    doc_request = jsonable_encoder(doc_request)
    doc_request_saved = await add_request(doc_request)
    doc_request_saved["_id"] = str(doc_request_saved["_id"])
    doc_uploaded_content = await read_file_s3(object_name)
    doc_uploaded_content = jsonable_encoder(doc_uploaded_content)
    content_received_from_ml = await sending_ml(doc_uploaded_content)
    content_received_from_ml = jsonable_encoder(content_received_from_ml)
    response_data_added = {
                "user_id": doc_request_saved["user_id"],
                "request_id": doc_request_saved["_id"] ,
                "prompt": doc_uploaded_content,
                "ml_response": content_received_from_ml,
                "isSuccess": True
            }
    response_data_added = jsonable_encoder(response_data_added)
    response_saved  = await add_response(response_data_added)
    response_saved["_id"] = str(response_saved["_id"])
    return response_saved


async def add_user_data(user : UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    new_user["_id"]= str(new_user["_id"])
    return new_user

async def add_request_data(request : RequestSchema = Body(...)):
    request = jsonable_encoder(request)
    new_request = await add_request(request)
    new_request["_id"] = str(new_request["_id"] )
    return new_request


async def add_response_data(response : ResponseSchema = Body(...)):
    response = jsonable_encoder(response)
    new_response = await add_response(response)
    new_response["_id"] = str(new_response["_id"] )
    return new_response