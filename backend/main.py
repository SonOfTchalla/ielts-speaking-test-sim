from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import whisper
import openai
import json
from pydantic import BaseModel
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class SpeechInput(BaseModel):
    transcript: str

@app.get("/")
def read_root():
    return {"message": "IELTS Speaking Test Simulator API"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an IELTS examiner."},
                      {"role": "user", "content": data}]
        )
        examiner_reply = response['choices'][0]['message']['content']
        await websocket.send_text(examiner_reply)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    model = whisper.load_model("base")
    audio = await file.read()
    with open("temp_audio.wav", "wb") as f:
        f.write(audio)
    result = model.transcribe("temp_audio.wav")
    return {"transcript": result["text"]}