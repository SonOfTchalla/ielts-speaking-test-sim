from transformers import pipeline

evaluation_pipeline = pipeline("text-classification", model="HuggingFaceScoringModel")

def evaluate_response(transcript: str):
    feedback = evaluation_pipeline(transcript)
    return {"feedback": feedback[0]["label"]}