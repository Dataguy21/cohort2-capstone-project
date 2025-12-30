# src/genai_interface.py
"""
GenAI Interface using Google Gemini API (with .env key loading)
"""

import os
from google import genai
from dotenv import load_dotenv

# ✅ Load .env variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found! Please add it to your .env file.")

# ✅ Initialize Gemini client
client = genai.Client(api_key=API_KEY)


def summarize_doctor_notes(notes_list, model="gemini-2.0-flash"):
    if not notes_list:
        return "No doctor notes found."

    joined_notes = "\n".join(notes_list[:200])
    prompt = f"""
Summarize the following clinical doctor notes:

{joined_notes}

Summarize into:
1. Key observations
2. Common adverse events
3. Positive improvements
4. Outliers or anomalies
"""
    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini API Error: {str(e)}"


def generate_regulatory_summary(trial_text, model="gemini-2.0-flash"):
    prompt = f"""
Write a 3-paragraph FDA-style summary of the following clinical trial results:

{trial_text}

Cover:
1. Compliance and patient outcomes
2. Adverse events or issues
3. Final interpretation and next steps
"""
    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini API Error: {str(e)}"
