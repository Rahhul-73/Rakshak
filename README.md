# 🛡️ Rakshak (रक्षक) - Complete AI UPI Scam Detection Ecosystem

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Ecosystem](https://img.shields.io/badge/Platforms-Telegram%20%7C%20Streamlit%20%7C%20Flask-purple.svg)
![AI Model](https://img.shields.io/badge/AI-Google%20Gemini%201.5%20Flash-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Rakshak** ("Protector" in Sanskrit) is a 3-in-1 AI security ecosystem designed to safeguard 500M+ Indian citizens against financial fraud, smishing, fake lottery traps, KYC blocking threats, and wrong transfer scams.

---

## 🌐 3-in-1 Ecosystem Architecture

1. 🤖 **Telegram Bot (`bot.py`)**: Users forward suspicious SMS/WhatsApp messages directly on Telegram for instant analysis.
2. 🎨 **Streamlit Web App (`web_app.py`)**: Interactive web interface featuring dark-theme cards, gTTS Hindi voice warning audio, and real-time session analytics.
3. ⚡ **Flask Web App & REST API (`flask_app.py`)**: Lightweight web server and HTML/CSS/JS frontend with `/api/analyze` REST API endpoint.

---

## 📁 Repository Structure

```
RAKSHAK/
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies (Flask, Streamlit, Gemini, gTTS)
├── config.py           # Configuration (Streamlit secrets, .env fallback & prompt)
├── detector.py         # Dual-engine detector (Regex quick scan + Gemini AI)
├── bot.py              # Telegram Bot handlers & polling engine
├── web_app.py          # Streamlit Web Application
├── flask_app.py        # Flask Web Server & REST API backend
├── templates/
│   └── index.html      # HTML5/CSS3/JS dark-theme frontend for Flask
├── test_detector.py    # Local test suite
└── README.md           # Documentation & deployment guide
```

---

## 🚀 How to Run Each Platform Locally

### 1. Setup Virtual Environment & API Keys
```bash
cd /Users/rahulvoruganti/Desktop/RAKSHAK
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Edit `.env` and insert your tokens:
```env
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
TELEGRAM_BOT_TOKEN=7123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

---

### 2. Launch Streamlit Web App
```bash
streamlit run web_app.py
```
Access at `http://localhost:8501`.

---

### 3. Launch Flask Web App & REST API
```bash
python flask_app.py
```
Access at `http://127.0.0.1:5000`.

**REST API Endpoint:**
`POST http://127.0.0.1:5000/api/analyze`
```json
{
  "message": "Your Paytm KYC is pending. Update now: bit.ly/kyc"
}
```

---

### 4. Launch Telegram Bot
```bash
python bot.py
```

---

## 🌐 Deploying to Cloud

### 1. Streamlit Community Cloud (Free Streamlit Deployment)
- Push repository to GitHub.
- Connect on [share.streamlit.io](https://share.streamlit.io) -> Select `web_app.py`.
- Add `GEMINI_API_KEY` under **App Settings -> Secrets**.

### 2. Render.com / PythonAnywhere (Flask / Telegram Bot)
- Render Web Service for Flask: Start Command `python flask_app.py`.
- Render Background Worker for Telegram: Start Command `python bot.py`.

---

## 🚨 Emergency Cybercrime Helpline
- 📞 **Helpline**: Call **1930** (Toll-Free, 24x7)
- 🌐 **Portal**: [cybercrime.gov.in](https://cybercrime.gov.in)
