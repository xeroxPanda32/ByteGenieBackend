from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse


from server.database import (
  get_all_responses)
    
router = APIRouter()

from server.routes.controller import (
    responseDetail,
    upload_file_generate_response,
    add_user_data,
    add_request_data,
    add_response_data
)

@router.get('/responsedetails', response_model=dict)
async def get_response_detail(response_detail_result: dict = Depends(responseDetail)):
    return JSONResponse(content=response_detail_result)

@router.get('/allResponses')
async def allResponses():
    all_responses_received = await get_all_responses()
    return all_responses_received

@router.post("/uploadfile/",response_model=dict)
async def get_ml_response(uploadFile_andGenerate: dict = Depends(upload_file_generate_response)):
    return JSONResponse(content=uploadFile_andGenerate) 

@router.post("/adduser",response_model=dict)
async def add_new_user(add_user: dict = Depends(add_user_data)):
    return JSONResponse(content=add_user) 

@router.post("/addrequest",response_description="Request data added into the database")
async def add_new_request(add_request: dict = Depends(add_request_data)):
    return JSONResponse(content=add_request)

@router.post("/addresponse",response_description="Response data added into the database")
async def add_new_response(add_response: dict = Depends(add_response_data)):
    return JSONResponse(content=add_response)