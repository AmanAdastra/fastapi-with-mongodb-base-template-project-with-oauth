from fastapi_jwt_auth import AuthJWT
import json
from datetime import timedelta
from common_layer import constants
from passlib.context import CryptContext
from schemas import common_schema

pwd_cxt= CryptContext(schemes=["bcrypt"], deprecated = "auto")
settings = common_schema.Settings()


class Hash():
    def bcrypt(password:str):
        return pwd_cxt.hash(password)
    def Verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)



def extract_user_detail_from_jwt(jwt_token: AuthJWT):
    user_info = json.loads(jwt_token.get_jwt_subject().replace("'", '"').replace("ObjectId(", "").replace(")", ""))
    user_id = user_info["id"]
    email_id = user_info["email_id"]
    return (user_id), email_id

def refresh_token(authorize: AuthJWT):
    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user, expires_time=timedelta(seconds=constants.ACCESS_TOKEN_EXPIRY_TIME))
    refresh_token = authorize.create_refresh_token(subject = current_user, expires_time=timedelta(seconds=constants.REFRESH_TOKEN_EXPIRY_TIME))
    return {"access_token": new_access_token, "new_refresh_token":refresh_token}