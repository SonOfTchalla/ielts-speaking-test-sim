from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from vosk import Model, KaldiRecognizer
import json
import os
import wave
import requests
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HF_HEADERS = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
vosk_model = Model("model")


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
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": data})
        response_json = response.json()
        examiner_reply = response_json["generated_text"] if "generated_text" in response_json else "I didn't understand that."
        await websocket.send_text(examiner_reply)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    audio = await file.read()
    with open("temp_audio.wav", "wb") as f:
        f.write(audio)
    wf = wave.open("temp_audio.wav", "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    rec.SetWords(True)
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)
    result = json.loads(rec.FinalResult())
    return {"transcript": result["text"]}

@app.post("/evaluate/")
def evaluate_response(speech: SpeechInput):
    response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": f"Evaluate this IELTS speaking response: {speech.transcript}"})
    feedback = response.json().get("generated_text", "Feedback not available.")
    return {"feedback": feedback}