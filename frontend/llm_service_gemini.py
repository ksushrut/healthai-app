# llm_service_gemini.py
import os
from typing import Dict, Any
import google.generativeai as genai

def _init():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # If you keep secrets in Streamlit, you can import streamlit and read st.secrets here
        # import streamlit as st
        # api_key = st.secrets["GOOGLE_API_KEY"]
        raise RuntimeError("GOOGLE_API_KEY not set")
    genai.configure(api_key=api_key)

def generate_coach_reply(profile: Dict[str, Any], user_question: str) -> str:
    """
    profile: dict of inputs captured from _2_Profile.py
    user_question: free-form question, or auto-generated prompt
    """
    _init()
    model = genai.GenerativeModel("gemini-1.5-pro")  # or "gemini-1.5-flash" for faster/cheaper

    # Keep only the fields you actually have (avoid None to reduce token bloat)
    safe_profile = {k: v for k, v in profile.items() if v not in (None, "", [])}

    system = (
        "You are a concise, practical health & meal-planning assistant. "
        "Give actionable steps, short bullet points, and avoid medical claims."
    )

    prompt = (
        f"{system}\n\n"
        f"User profile (use to personalize your answer):\n{safe_profile}\n\n"
        f"User question/request:\n{user_question}\n\n"
        f"Constraints: Keep it concise. If you recommend numbers (calories/macros), clearly label them."
    )

    resp = model.generate_content(prompt)
    return (resp.text or "").strip()
