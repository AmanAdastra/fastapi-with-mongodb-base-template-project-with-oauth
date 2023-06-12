from database import db
from schemas.user_authentication_schema import UserRegisterRequest , UserLoginRequest, UserInfoRequest
from schemas.common_schema import CommonResponseSchema
from http import HTTPStatus
from logging_module import logger
from common_layer import utils, constants
from datetime import timedelta
from fastapi_jwt_auth import AuthJWT

def register_customer(request:UserRegisterRequest, authorize:AuthJWT):
    logger.debug("Inside Register Customer Service")
    customer_collection = db["customer_details"]

    if customer_collection.find_one({"email": request.email }):
        response = CommonResponseSchema(
        type= "Failed", status_code= HTTPStatus.CONFLICT, message="Email already assigned to other user.", data={}
    )
        return response

    if request.password != request.confirm_password:
        response = CommonResponseSchema(
        type= "Failed", status_code= HTTPStatus.CONFLICT, message="Password and Confirm password didn't match.", data={}
    )
        return response
    request.password = utils.Hash.bcrypt(request.password)
    data = {
        "username": request.name,
        "email": request.email,
        "password": request.password
    }
    response = customer_collection.insert_one(data)
    sub = {"email": request.email, "id": str(response.inserted_id)}
    access_token = authorize.create_access_token(
            subject=str(sub), expires_time=timedelta(seconds=constants.ACCESS_TOKEN_EXPIRY_TIME))
    refresh_token = authorize.create_refresh_token(subject=str(sub), expires_time=timedelta(seconds=constants.REFRESH_TOKEN_EXPIRY_TIME))
    response = CommonResponseSchema(
        type= "Success", status_code= HTTPStatus.CREATED, message="User Created Successfully", data={
            "access_token": access_token, "refresh_token": refresh_token
        }
    )
    logger.debug("Returning From Register Customer Service")
    return response

def login_customer(request:UserLoginRequest, authorize:AuthJWT):
    logger.debug("Inside Customer Login Service")
    customer_collection = db["customer_details"]
    user = customer_collection.find_one({"email":request.email})
    if user is None:
        response = CommonResponseSchema(
        type= "Failed", status_code= HTTPStatus.CONFLICT, message="Email not Found.", data={}
    )
        return response
    
    if not utils.Hash.Verify(hashed_password= user.get("password") ,plain_password=request.password):
        response = CommonResponseSchema(
        type= "Failed", status_code= HTTPStatus.CONFLICT, message="Incorrect Password", data={}
    )
        return response

    sub = {"email": user['email'], "id": str(user['_id']) }
    access_token = authorize.create_access_token(
            subject=str(sub), expires_time=timedelta(seconds=constants.ACCESS_TOKEN_EXPIRY_TIME))
    refresh_token = authorize.create_refresh_token(subject=str(sub), expires_time=timedelta(seconds=constants.REFRESH_TOKEN_EXPIRY_TIME))
    response = CommonResponseSchema(
        type= "Success", status_code= HTTPStatus.ACCEPTED, message="User Logged in Successfully", data={
            "username": user.get("username"),"access_token": access_token, "refresh_token": refresh_token
        }
    )
    logger.debug("Returning From Customer Login Service")
    return response

def get_customer(email, authorize:AuthJWT):
    logger.debug("Inside Customer Info Service")
    customer_collection = db["customer_details"]
    user = customer_collection.find_one({"email":email})
    if user is None:
        response = CommonResponseSchema(
        type= "Failed", status_code= HTTPStatus.CONFLICT, message="Email not Found.", data={}
    )
        return response
    data = {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "email": user.get("email")
    }
    response = CommonResponseSchema(
        type= "Success", status_code= HTTPStatus.ACCEPTED, message="User Data Fetched Successfully", data=data
    )
    logger.debug("Returning From Customer Info Service")
    return response
