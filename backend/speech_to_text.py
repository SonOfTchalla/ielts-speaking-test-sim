from vosk import Model, KaldiRecognizer
import wave

model = Model("vosk-model-small-en-us-0.15")  # Download from Vosk website

def transcribe_audio(file_path):
    wf = wave.open(file_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if not data:
            break
        rec.AcceptWaveform(data)

    result = rec.Result()
    return result
