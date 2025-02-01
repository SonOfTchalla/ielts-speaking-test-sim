from transformers import pipeline

qa_pipeline = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct")

def get_ai_response(user_input):
    response = qa_pipeline(user_input, max_length=200)[0]["generated_text"]
    return response
