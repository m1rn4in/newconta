
#Python
from pydantic import BaseModel, EmailStr
from typing import Optional

class Message(BaseModel):
    text: str
    
class AccessToken(BaseModel):
    access_token: str
    token_type: str


class AccessAndRefreshToken(AccessToken):
    refresh_token: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UpdatePassword(BaseModel):
    new_password: str
    password_confirmation: str


class ForgotPasswordEmail(BaseModel):
    email:EmailStr