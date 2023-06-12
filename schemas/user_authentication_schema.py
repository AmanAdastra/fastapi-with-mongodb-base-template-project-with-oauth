from pydantic import BaseModel
from typing import Optional, Any
from pydantic import EmailStr

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserInfoRequest(BaseModel):
    email: EmailStr