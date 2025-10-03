import os
from dotenv import load_dotenv  
load_dotenv()  # Load environment variables from .env file
import google.generativeai as genai  # <-- Gemini API
API_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_key)
def apply_prompt(query, retrieved_answer):
    """
    Generate a personality-driven response using Gemini API.
    KB is used only as reference; LLM rephrases logically.
    """
    prompt = f"""
You are Aditi Sharma’s AI voice assistant.
Your goal is to answer interview-style questions on Aditi’s behalf.

Question: {query}

Knowledge Base Reference:
{retrieved_answer}

Instructions:
- Always base your response on the Knowledge Base reference.
- Do not copy the KB text verbatim, rephrase it naturally in first person.
- If the KB is relevant, weave it directly into the answer.
- If KB is empty or irrelevant, politely redirect the conversation.
- Respond as Aditi, in a confident, authentic, and warm tone.
- Keep answers concise but detailed (3–5 sentences).
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    
    return response.text
