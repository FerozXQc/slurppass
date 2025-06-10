from fastapi import APIRouter, Form, Cookie, Response, HTTPException, Request
from schemas import RegisterUserSchema, LoginUserSchema
from database import db_createUser
from redis_client import create_sessions, get_user_name, delete_session
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
            return {"result": f"email already exists: {email}",
                    'loggable':False
                    }

        if utility.check_user_exists(name):
            return {'result': f'username already exists: {name}','loggable':False}

        hashed_password = hashargon.generate_hash(password)
        print(hashed_password)  ##for debugging..
        result = db_createUser(name,email,hashed_password)
        return {"result": result,
        'loggable':True}
    else:
        return {"result": "email is not valid!!"}

@auth_router.get('/me')
def me(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=403, detail="login expired/unauthorized")
    user_id = get_user_name(session_id)
    if user_id:
        return {"user": user_id}
    raise HTTPException(status_code=403, detail="login expired/unauthorized")

@auth_router.post("/login")
def login(userSchema: LoginUserSchema, response: Response):
    email, password = userSchema.email, userSchema.password
    user = utility.get_user_by_email(email)
    print(user) #debugging
    if not user:
        return {"message": "No user found with that email!", "status_code":403}
    isverified = hashargon.verify_hash(user.password, password) #verify_hash(hashed_password,password)
    if not isverified:
        return {"message":"invalid password. Please try again.", "status_code":403}
    else:
        session_id = create_sessions(user.name)
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=86400)
        return {"message": "login successful", "session_id": session_id, "user": user.name}


@auth_router.post("/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(session_id)
        response.delete_cookie("session_id")
    return {"message": "logged out"}
