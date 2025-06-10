from pydantic import BaseModel 
##for fastapi
class RegisterUserSchema(BaseModel):
    name: str
    email: str
    password: str  #passwords stored in db are hashed

class LoginUserSchema(BaseModel):
    email: str
    password: str   

class AddPassLog(BaseModel):
    user_id:str
    title:str
    desc:str
    passlog:str