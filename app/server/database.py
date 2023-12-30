from pymongo import MongoClient
from bson.objectid import ObjectId
import motor.motor_asyncio
from decouple import config


from server.config.config import (
  MONGO_URI
)
 
uri_parts = MONGO_URI.split("?")
uri_without_options = uri_parts[0]

client = motor.motor_asyncio.AsyncIOMotorClient(uri_without_options)

database = client["byteDoc"]

user_collection = database["users_collection"]

request_collection = database["requests_collection"]

response_collection = database["responses_collection"]



# Add a new user to the database
async def add_user(user_data: dict)-> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id" : user.inserted_id})
    return new_user

# Add new requset to the database
async def add_request(request_data: dict)-> dict:
    request = await request_collection.insert_one(request_data)
    new_request = await request_collection.find_one({"_id" : request.inserted_id})
    return new_request

# Add new response to the database
async def add_response(response_data: dict)-> dict:
    response = await response_collection.insert_one(response_data)
    new_response = await response_collection.find_one({"_id" : response.inserted_id})
    return new_response


# get a response from the database
async def get_response(id : str):
    try:
        result = await response_collection.find_one({"_id": ObjectId(id)})
        if(result):
            requestId = result["request_id"]
            request = await request_collection.find_one({"_id": ObjectId(requestId)})
            request["_id"] = str(request["_id"])
            result["request_id"] = request
            return result
        else:
            return False
    except Exception as e:
        print(f"Error in get_all_responses: {e}")
        return False

# get all response from the database
async def get_all_responses():
    try:
        cursor = response_collection.find()
        responses = await cursor.to_list(length=None)
        for response in responses:
            response["_id"] = str(response["_id"])
        return responses
    except Exception as e:
        print(f"Error in get_all_responses: {e}")
        return None

   







