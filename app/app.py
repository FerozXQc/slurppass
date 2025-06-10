from fastapi import FastAPI
import uvicorn
from auth_routes import auth_router
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.add_middleware(SessionMiddleware, secret_key="some-super-secret-key")


app.include_router(auth_router, prefix="/auth")

@app.get("/")
def hello():
    return "hello"


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
