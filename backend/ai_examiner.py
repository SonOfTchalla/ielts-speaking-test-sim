from transformers import pipeline

examiner_pipeline = pipeline("text-generation", model="google/flan-t5-small", device_map="cpu")


def generate_examiner_response(user_input: str):
    response = examiner_pipeline(user_input, max_length=150)
    return response[0]["generated_text"]