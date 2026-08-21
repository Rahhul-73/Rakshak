"""
Rakshak - Scam Detection Engine
Hybrid detection engine combining Regex Quick Scan and Google Gemini 1.5 Flash AI.
"""

import re
import json
import logging
from config import GEMINI_API_KEY, SCAM_DETECTION_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RakshakDetector")

# Import Gemini SDK (prefer modern google-genai, fallback to google.generativeai)
GENAI_CLIENT = None
USE_NEW_SDK = False

if GEMINI_API_KEY:
    try:
        from google import genai
        GENAI_CLIENT = genai.Client(api_key=GEMINI_API_KEY)
        USE_NEW_SDK = True
        logger.info("Using new google-genai SDK.")
    except Exception:
        try:
            import google.generativeai as genai_old
            genai_old.configure(api_key=GEMINI_API_KEY)
            GENAI_CLIENT = genai_old
            USE_NEW_SDK = False
            logger.info("Using legacy google.generativeai SDK.")
        except Exception as e:
            logger.warning(f"Could not initialize Gemini SDK: {e}")
else:
    logger.warning("GEMINI_API_KEY is missing in environment variables!")

# Regex patterns for high-confidence quick scanning
QUICK_SCAN_PATTERNS = [
    # KYC & Account Block
    (r"(?i)\bkyc\b.*(update|pending|verify|expire|blocked|suspend)", "KYC Scam", "Urgent requirement to update KYC/account status"),
    (r"(?i)(account|card|sim|banking|netbanking).*(block|suspend|deactivate|frozen)", "KYC/Account Scam", "Threat to block account/card/SIM"),
    (r"केवाईसी|खाता.*ब्लॉक|सिम.*ब्लॉक", "KYC Scam", "Hindi alert for KYC/account block"),

    # Lottery & Prizes
    (r"(?i)(congratulations|won|winner).*(lakh|crore|prize|lottery|kbc|car|reward)", "Lottery Scam", "Claim of winning huge prize/lottery"),
    (r"जीत.*(करोड़|लाख|इनाम|लॉटरी)|केबीसी.*जीत", "Lottery Scam", "Hindi claim of lottery/KBC winnings"),

    # Phishing Links & Refunds
    (r"(?i)(refund|cashback|bonus|free.*recharge).*(click|link|claim)", "Phishing", "Enticement to click link for refund/cashback"),
    (r"(?i)(bit\.ly|tinyurl\.com|t\.co|cutt\.ly|is\.gd|goo\.gl|shorturl|\.apk)", "Phishing Link", "Suspicious shortened link or APK file"),
    (r"(?i)(verify|update).*(pan|aadhaar|bank).*link", "Phishing", "Link asking to verify PAN/Aadhaar/Bank credentials"),

    # OTP Sharing & Screen Share
    (r"(?i)(share|tell|send|forward).*(otp|pin|password|cvv)", "Phishing/OTP Scam", "Demand to share OTP or PIN"),
    (r"(?i)(download|install).*(anydesk|teamviewer|rustdesk|quicksupport)", "Screen Sharing Scam", "Request to install remote screen sharing software"),
    (r"साझा.*(ओटीपी|पिन)|ओटीपी.*(शेयर|बताएं)", "OTP Scam", "Hindi demand to share OTP/PIN"),

    # Wrong Transfer Scam
    (r"(?i)(sent|transferred|credited|paid).*(by mistake|wrongly|accidentally|by accident)", "Wrong Transfer Scam", "Claim of accidental money transfer asking for return"),
    (r"(?i)(mistake|wrongly|accidental).*(sent|transferred|credited|paid|money)", "Wrong Transfer Scam", "Claim of accidental payment transfer"),
    (r"(?i)(return|send back|refund).*(to.*upi|to.*number|money|amount|rs|₹)", "Wrong Transfer Scam", "Pressure to return alleged accidental transfer"),
    (r"गलत.*(ट्रांसफर|क्रेडिट|पेमेंट)|गलती से.*(पैसे|रुपये).*(भेज|ट्रांसफर)", "Wrong Transfer Scam", "Hindi claim of accidental payment transfer"),

    # Urgent Actions & Fees
    (r"(?i)(urgent|immediately|within 24 hours|limited time|act now)", "Phishing", "Artificial panic and rush tactics"),
    (r"(?i)(pay|send|deposit).*(processing fee|registration fee|tax|security deposit)", "Fee Scam", "Demand for advance fee via UPI")
]

def quick_scan(message_text: str) -> dict:
    """
    Performs fast regex-based rule check on suspicious text.
    Returns matched patterns and confidence indicators.
    """
    text = message_text.strip()
    matched_flags = []
    detected_types = set()

    for pattern, scam_type, flag_description in QUICK_SCAN_PATTERNS:
        if re.search(pattern, text):
            matched_flags.append(flag_description)
            detected_types.add(scam_type)

    if matched_flags:
        primary_type = list(detected_types)[0]
        return {
            "is_suspicious": True,
            "detected_type": primary_type,
            "red_flags": matched_flags
        }
    
    return {
        "is_suspicious": False,
        "detected_type": None,
        "red_flags": []
    }

def detect_scam(message_text: str) -> dict:
    """
    Analyzes message using Gemini AI with regex quick-scan pre-filtering.
    Returns structured analysis dict.
    """
    # 1. Quick regex scan pre-check
    quick_res = quick_scan(message_text)

    # 2. If Gemini API Key is missing or client not initialized, rely on Quick Scan fallback
    if not GEMINI_API_KEY or not GENAI_CLIENT:
        if quick_res["is_suspicious"]:
            return {
                "is_scam": True,
                "risk_score": "High",
                "scam_type": quick_res["detected_type"],
                "red_flags": quick_res["red_flags"],
                "explanation": f"Quick scan detected high-risk scam patterns matching {quick_res['detected_type']}.",
                "action": "Do not click any links, do not share OTP, and do not send money.",
                "hindi_warning": "सावधान! यह एक संभावित धोखा हो सकता है। कोई ओटीपी या पैसा न भेजें।",
                "quick_scan_triggered": True
            }
        else:
            return {
                "is_scam": False,
                "risk_score": "Low",
                "scam_type": "None",
                "red_flags": [],
                "explanation": "No suspicious regex patterns found. (Configure GEMINI_API_KEY for full AI analysis)",
                "action": "Be cautious when receiving unsolicited messages from unknown senders.",
                "hindi_warning": "कोई संदिग्ध पैटर्न नहीं मिला। अज्ञात नंबरों से सावधान रहें।",
                "quick_scan_triggered": False
            }

    # 3. Full Gemini AI Analysis
    try:
        prompt = SCAM_DETECTION_PROMPT.format(message_text=message_text)

        if USE_NEW_SDK:
            response = GENAI_CLIENT.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            response_text = response.text.strip()
        else:
            model = GENAI_CLIENT.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config={"temperature": 0.1}
            )
            response_text = response.text.strip()
        
        # Clean potential markdown code formatting
        if response_text.startswith("```"):
            response_text = re.sub(r"^```[a-zA-Z]*\n", "", response_text)
            response_text = re.sub(r"\n```$", "", response_text).strip()
            
        data = json.loads(response_text)

        # Merge Quick Scan red flags if AI missed any
        if quick_res["is_suspicious"]:
            existing_flags = set(data.get("red_flags", []))
            for q_flag in quick_res["red_flags"]:
                if q_flag not in existing_flags:
                    data.setdefault("red_flags", []).append(q_flag)

        data["quick_scan_triggered"] = quick_res["is_suspicious"]
        return data

    except Exception as e:
        logger.error(f"Gemini API Analysis Error: {e}")
        
        # Fallback to Quick Scan result on API failure
        if quick_res["is_suspicious"]:
            return {
                "is_scam": True,
                "risk_score": "High",
                "scam_type": quick_res["detected_type"],
                "red_flags": quick_res["red_flags"],
                "explanation": "High-risk scam keywords detected by security filters.",
                "action": "Do not click any link or send money.",
                "hindi_warning": "सावधान! यह एक फर्जी संदेश लग रहा है।",
                "quick_scan_triggered": True
            }
        
        return {
            "is_scam": False,
            "risk_score": "Low",
            "scam_type": "None",
            "red_flags": [],
            "explanation": "Could not complete full AI scan due to network/API error.",
            "action": "Never share your UPI PIN or bank OTP with anyone.",
            "hindi_warning": "तकनीकी समस्या के कारण जांच पूर्ण नहीं हो सकी। सतर्क रहें।",
            "quick_scan_triggered": False
        }
