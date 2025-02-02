from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from pydantic import BaseModel
from ai_examiner import generate_examiner_response
from speech_to_text import transcribe_audio
from scoring import evaluate_response
from feedback import generate_feedback

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from client: {data}")  # Debugging log
            response = f"Server received: {data}"
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected")
