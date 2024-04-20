import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


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
    responses = [
        {"from": "chatGpt", "data": message.message, "format": "text"},
        {"from": "chatGpt", "data": message.message, "format": "code"},
    ]
    return responses

