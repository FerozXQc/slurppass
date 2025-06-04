from fastapi import APIRouter, Form, Cookie, Response, HTTPException, Request
from schemas import RegisterUserSchema, LoginUserSchema
from database import db_createUser
from redis_client import create_sessions, get_user_email, delete_session
from decouple import config
from database import UtilityFunctions, HashArgon

#assigning variables to the classes.
utility = UtilityFunctions 
hashargon = HashArgon

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/register")
def registerUser(user: RegisterUserSchema):
    name, email, password = user.name, user.email, user.password
    emailInfo = utility.is_validEmail(email)
    if emailInfo:
        if utility.get_user_by_email(emailInfo):
            return {"result": f"user already exists: {email}"}
        hashed_password = hashargon.generate_hash(password)
        print(hashed_password)  ##for debugging..
        result = db_createUser(name,email,hashed_password)
        return {"result": result}
    else:
        return {"result": "email is not valid!!"}

def me(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=403, detail="login expired/unauthorized")
    user_id = get_user_id(session_id)
    if user_id:
        return {"user": user_id}
    raise HTTPException(status_code=403, detail="login expired/unauthorized")

@auth_router.post("/login")
def login(userSchema: LoginUserSchema, response: Response):
    email, password = userSchema.email, userSchema.password
    user = utility.get_user_by_email(email)
    print(user) #debugging
    if not user:
        print("No user found with that email!")
        return
    isverified = hashargon.verify_hash(user.password, password) #verify_hash(hashed_password,password)
    if not isverified:
        return "invalid password. Please try again."
    else:
        session_id = create_sessions(user.name)
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return {"message": "login successful", "session_id": session_id}


@auth_router.post("/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(session_id)
        response.delete_cookie("session_id")
    return {"message": "logged out"}
