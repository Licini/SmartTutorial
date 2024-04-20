import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from query import init, ask

app = FastAPI()
origins = ["*"]

query_engine = init()

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
    global query_engine
    
    message.message = ask(query_engine, message.message)

    responses = [
        {"from": "chatGpt", "data": message.message, "format": "text"},
        # {"from": "chatGpt", "data": message.message, "format": "code"},
    ]
    return responses
