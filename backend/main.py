from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SpeechInput(BaseModel):
    transcript: str

@app.get("/")
def read_root():
    return {"message": "IELTS Speaking Test Simulator API"}