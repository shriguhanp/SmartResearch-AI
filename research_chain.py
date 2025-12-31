import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 🔹 Automatically select a working model
def get_working_model():
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            return genai.GenerativeModel(model.name)
    raise Exception("No supported Gemini models found for this API key.")

model = get_working_model()

def run_research(query: str):
    prompt = f"""
You are an AI research assistant.

Research Query:
{query}

Tasks:
1. Explain the topic clearly
2. Provide key insights
3. Mention real-world use cases
4. Give a short conclusion

Return the response in bullet points.
"""
    response = model.generate_content(prompt)
    return response.text
