from fastapi import APIRouter, Depends
from services import user_authentication_service
from schemas import common_schema, user_authentication_schema
from logging_module import logger
from fastapi_jwt_auth import AuthJWT
from pydantic import EmailStr
from common_layer import utils
router = APIRouter(
    prefix="/user",
    tags=["User Authentication"],
    responses={404: {"description": "Url Not found"}},
)


@router.get("/get-customer",response_model= common_schema.CommonResponseSchema)
def get_customer(email: EmailStr, authorize: AuthJWT = Depends()):
    logger.debug("Inside Get Customer Router")
    authorize.jwt_optional()
    response = user_authentication_service.get_customer(email, authorize)
    logger.debug("Returning From Get Customer Router")
    return response

@router.post("/register-customer",response_model= common_schema.CommonResponseSchema)
def register_customer(request: user_authentication_schema.UserRegisterRequest, authorize: AuthJWT = Depends()):
    logger.debug("Inside Register Customer Register Router")
    authorize.jwt_optional()
    response = user_authentication_service.register_customer(request ,authorize)
    logger.debug("Returning From Customer Register Router")
    return response

@router.post("/login-customer",response_model= common_schema.CommonResponseSchema)
def login_customer(request: user_authentication_schema.UserLoginRequest, authorize: AuthJWT = Depends()):
    logger.debug("Inside Login Customer Router")
    response = user_authentication_service.login_customer(request,authorize)
    logger.debug("Returning From Login Customer Router")
    return response


@router.post("/refresh-token")
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    response = utils.refresh_token(authorize)
    return response