from pydantic import BaseModel,Field,field_validator
from app.services.auth_service import normalize_username


class LoginRequest(BaseModel):
    username:str=Field(min_length=1,max_length=64)
    password:str=Field(min_length=1,max_length=128)

class RegisterRequest(BaseModel):
    username:str=Field(min_length=3,max_length=32)
    password:str=Field(min_length=8,max_length=128)

    @field_validator("username")
    @classmethod
    def validate_user(cls,value:str) -> str:
        username=normalize_username(value)
        if not 3<= len(username) <=32:
            raise ValueError("用户名需为3-32字符")
        if any(not(char.isalnum() or char in "_-") for char in username):
            raise ValueError("用户名只能包含文字、字母、数字、下划线或短横线")
        return username


class LoginResponse(BaseModel):
    token:str
    user_id:int
    username:str
    is_admin:bool
