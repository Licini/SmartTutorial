import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ask import ask

app = FastAPI()
origins = ["*"]


class Message(BaseModel):
    message: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/")
async def echo_message(message: Message):
    
    message.message = ask(message.message)

    responses = [
        {"from": "chatGpt", "data": message.message},
    ]
    return responses
