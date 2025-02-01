from fastapi import UploadFile, File
import vosk
import wave
import json

def transcribe_audio(file: UploadFile):
    model = vosk.Model("model_path")
    wf = wave.open(file.file, "rb")
    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)
    result = json.loads(rec.Result())
    return {"transcript": result["text"]}