"""
Rakshak (रक्षक) - AI UPI Scam Detector Web Application
Powered by Streamlit, Google Gemini AI, and gTTS
"""

import io
import streamlit as st
from gtts import gTTS
from config import CYBERCRIME_HELPLINE, CYBERCRIME_PORTAL
from detector import detect_scam

# 1. Page Configuration
st.set_page_config(
    page_title="Rakshak | AI UPI Scam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Fintech Dark Theme Aesthetics
st.markdown("""
    <style>
    /* Dark Theme Backgrounds */
    .stApp {
        background-color: #0a0e27;
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Custom Header Styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.15rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }

    /* Card Containers */
    .custom-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    /* Risk Cards */
    .risk-critical {
        border-left: 6px solid #dc2626 !important;
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, #0f172a 100%);
    }
    .risk-high {
        border-left: 6px solid #f97316 !important;
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, #0f172a 100%);
    }
    .risk-medium {
        border-left: 6px solid #eab308 !important;
        background: linear-gradient(135deg, rgba(234, 179, 8, 0.1) 0%, #0f172a 100%);
    }
    .risk-low {
        border-left: 6px solid #22c55e !important;
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, #0f172a 100%);
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-right: 0.5rem;
    }
    .badge-critical { background-color: #dc2626; color: white; }
    .badge-high { background-color: #f97316; color: white; }
    .badge-medium { background-color: #eab308; color: black; }
    .badge-low { background-color: #22c55e; color: white; }

    /* Hindi Warning Box */
    .hindi-box {
        background-color: #1e1b4b;
        border: 1px solid #4338ca;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }

    /* Streamlit Text Area Customization */
    .stTextArea textarea {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
    }

    /* Primary Button Gradient */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-size: 1.1rem !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }

    /* Helpline Banner */
    .helpline-card {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        text-align: center;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Session State Initialization for Analytics
if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0
if "scams_detected" not in st.session_state:
    st.session_state.scams_detected = 0
if "message_input" not in st.session_state:
    st.session_state.message_input = ""

# Callback helper for quick-fill buttons
def set_sample_message(text: str):
    st.session_state.message_input = text

# 4. Sidebar Content
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/shield.png", width=70)
    st.markdown("## 🛡️ Rakshak (रक्षक)")
    st.markdown("AI Security Shield for Indian UPI Users")
    st.divider()

    # Session Stats
    st.markdown("### 📊 Scan Session Analytics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Scans", value=st.session_state.total_scans)
    with col2:
        st.metric(label="Scams Found", value=st.session_state.scams_detected)

    st.divider()

    # Emergency Helpline
    st.markdown("### 🚨 Emergency Cybercrime Help")
    st.markdown(
        f"""
        <div class="helpline-card">
            <h3 style="margin:0; font-size: 1.5rem;">📞 Call {CYBERCRIME_HELPLINE}</h3>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.85rem;">National Cybercrime Toll-Free Helpline (24x7)</p>
            <a href="{CYBERCRIME_PORTAL}" target="_blank" style="color: #fef08a; font-weight: bold; text-decoration: underline;">Visit cybercrime.gov.in</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    st.markdown("### 💡 Golden Rule of UPI")
    st.info("🔒 **UPI PIN is ONLY required to SEND money.** You NEVER need to enter your PIN to receive money!")

    st.markdown("---")
    st.caption("Built with Google Gemini 1.5 Flash • Streamlit • Python")

# 5. Main Web App Header
st.markdown('<div class="main-title">🛡️ Rakshak — AI UPI Scam Detector</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Instantly analyze suspicious SMS, WhatsApp messages, or payment requests using Google Gemini AI</div>', unsafe_allow_html=True)

# 6. Quick Sample Test Buttons
st.markdown("##### 🧪 Quick Test Examples (Click to auto-fill):")
sample_cols = st.columns(4)

with sample_cols[0]:
    if st.button("📱 KYC Scam", key="sample_kyc"):
        set_sample_message("Your Paytm KYC is pending. Update now: bit.ly/kyc")
with sample_cols[1]:
    if st.button("🎁 Lottery Scam", key="sample_lottery"):
        set_sample_message("Congratulations! You won ₹10 Lakh in KBC. Send ₹5000 processing fee.")
with sample_cols[2]:
    if st.button("💸 Wrong Transfer", key="sample_wrong"):
        set_sample_message("Hi, I sent ₹50,000 to you by mistake. Please return to 9876543210@upi")
with sample_cols[3]:
    if st.button("✅ Safe Message", key="sample_safe"):
        set_sample_message("Hello, how are you? Are we meeting today at 5 PM?")

# 7. Message Input Form
st.markdown("### 📥 Message Text")
user_message = st.text_area(
    label="Paste or type suspicious message text below:",
    value=st.session_state.message_input,
    height=140,
    placeholder="e.g. Your SBI account is blocked due to pending KYC. Click here to verify: bit.ly/sbi-kyc..."
)

analyze_clicked = st.button("🔍 Analyze Message with AI", type="primary")

# 8. Analysis Output Logic
if analyze_clicked:
    if not user_message.strip():
        st.warning("⚠️ Please enter or paste a message to analyze!")
    else:
        with st.spinner("🤖 Scanning message with AI & Security Filters..."):
            result = detect_scam(user_message)
            
            # Update session stats
            st.session_state.total_scans += 1
            if result.get("is_scam", False):
                st.session_state.scams_detected += 1

        # Extract Result Fields
        is_scam = result.get("is_scam", False)
        risk_score = result.get("risk_score", "Medium")
        scam_type = result.get("scam_type", "Unknown Scam")
        red_flags = result.get("red_flags", [])
        explanation = result.get("explanation", "")
        action = result.get("action", "")
        hindi_warning = result.get("hindi_warning", "")

        # CSS Class for Risk Card
        risk_css_map = {
            "Critical": "risk-critical",
            "High": "risk-high",
            "Medium": "risk-medium",
            "Low": "risk-low"
        }
        card_class = risk_css_map.get(risk_score, "risk-medium")
        if not is_scam:
            card_class = "risk-low"

        # Badge Mapping
        badge_css_map = {
            "Critical": "badge-critical",
            "High": "badge-high",
            "Medium": "badge-medium",
            "Low": "badge-low"
        }
        badge_class = badge_css_map.get(risk_score, "badge-medium")

        # 9. Results Display Card
        st.markdown(f'<div class="custom-card {card_class}">', unsafe_allow_html=True)

        if is_scam:
            st.markdown(f"""
                <h2 style="color: #ef4444; margin-top: 0;">🚨 SCAM DETECTED!</h2>
                <p>
                    <span class="badge {badge_class}">Risk: {risk_score.upper()}</span>
                    <span class="badge" style="background-color: #334155; color: white;">Type: {scam_type}</span>
                </p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <h2 style="color: #22c55e; margin-top: 0;">✅ Message Appears SAFE</h2>
                <p>
                    <span class="badge badge-low">Risk: LOW</span>
                    <span class="badge" style="background-color: #334155; color: white;">Type: Legitimate Message</span>
                </p>
            """, unsafe_allow_html=True)

        st.markdown("#### 📖 Explanation")
        st.write(explanation)

        if red_flags:
            st.markdown("#### ⚠️ Red Flags Found:")
            for flag in red_flags:
                st.markdown(f"• **{flag}**")

        st.markdown("#### ✅ Recommended Action:")
        st.info(action)

        # Hindi Warning Card & Audio Playback
        if hindi_warning:
            st.markdown(f"""
                <div class="hindi-box">
                    <h4 style="margin:0 0 0.4rem 0; color: #a5b4fc;">🔊 Hindi Voice Warning (हिंदी चेतावनी)</h4>
                    <p style="font-size: 1.1rem; margin:0;"><em>"{hindi_warning}"</em></p>
                </div>
            """, unsafe_allow_html=True)

            # Generate gTTS Speech Audio
            try:
                tts = gTTS(text=hindi_warning, lang="hi")
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                st.audio(audio_fp, format="audio/mp3")
            except Exception as e:
                st.caption(f"Audio playback unavailable ({e})")

        st.markdown('</div>', unsafe_allow_html=True)

        # 10. Copyable Report Summary
        report_summary = (
            f"🛡️ Rakshak Analysis Report\n"
            f"Status: {'🚨 SCAM DETECTED' if is_scam else '✅ SAFE'}\n"
            f"Risk: {risk_score} | Type: {scam_type}\n"
            f"Explanation: {explanation}\n"
            f"Action: {action}\n"
            f"Report Cybercrime: Call 1930 or visit cybercrime.gov.in"
        )
        
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            st.caption("📋 Share / Save Report:")
            st.code(report_summary, language="text")

# 11. Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.9rem;">
        🛡️ <strong>Rakshak</strong> — Protecting Indian Citizens from Financial Fraud | Lost money? Call <strong>1930</strong> immediately.
    </div>
    """,
    unsafe_allow_html=True
)
