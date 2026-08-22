"""
Rakshak - Ecosystem Configuration & Prompt Templates
"""

import os

# Safely check Streamlit secrets first, then environment variables, then .env
GEMINI_API_KEY = None

try:
    import streamlit as st
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    except Exception:
        pass

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Cybercrime Helpline Info
CYBERCRIME_HELPLINE = "1930"
CYBERCRIME_PORTAL = "https://cybercrime.gov.in"

# Standardized System Prompt Template for Gemini AI
SCAM_DETECTION_PROMPT = """
You are "Rakshak" – an AI scam detector for Indian UPI users.

Analyze the following message and respond ONLY in this JSON format:

{{
  "is_scam": true/false,
  "risk_score": "Low/Medium/High/Critical",
  "scam_type": "KYC Scam/Lottery Scam/Phishing/Wrong Transfer/Fake UPI/Job Scam/Loan Scam/Other",
  "red_flags": ["list of suspicious indicators found in the message"],
  "explanation": "Simple explanation in plain English (max 50 words)",
  "action": "What the user should do next (max 30 words)",
  "hindi_warning": "Short warning in Hindi (max 20 words)"
}}

Message: "{message_text}"
"""
