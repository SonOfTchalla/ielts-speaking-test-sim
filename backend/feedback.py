from transformers import pipeline

feedback_pipeline = pipeline("text-generation", model="HuggingFaceFeedbackModel")

def generate_feedback(transcript: str):
    feedback = feedback_pipeline(transcript, max_length=100)
    return {"feedback": feedback[0]["generated_text"]}