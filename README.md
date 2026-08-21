# 🛡️ Rakshak (रक्षक) - AI UPI Scam Detector (Web App & Telegram Bot)

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Framework](https://img.shields.io/badge/Streamlit-v1.30%2B-red.svg)
![AI Model](https://img.shields.io/badge/AI-Google%20Gemini%201.5%20Flash-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Rakshak** ("Protector" in Sanskrit) is an open-source, AI-powered security application designed to safeguard Indian citizens against UPI payment frauds, smishing, phishing links, and social engineering attacks. It is available as both a **Streamlit Web Application** and a **Telegram Bot**.

---

## 🚀 Key Features

- 🎨 **Fintech Dark Theme Web Interface**: Built with Streamlit, custom dark mode styling (`#0a0e27` background, `#0f172a` cards, purple gradients).
- ⚡ **Dual-Engine Security**: Instant Regex Quick-Scanner + Google Gemini 1.5 Flash AI analysis.
- 📱 **Multi-Vector Fraud Detection**: Detects KYC blocking threats, Lottery/KBC traps, Wrong Transfer scams, Part-time job scams, Fake UPI PIN prompts, and APK malware links.
- 🔊 **Hindi Warning Audio Playback**: Generates on-the-fly Hindi audio warnings using `gTTS`.
- 📊 **Real-time Session Analytics**: Tracks total message scans and detected scams during user sessions.
- 🚨 **Emergency Helpline Direct Access**: Instant access to National Cybercrime Helpline `1930` and official reporting portals.

---

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Web UI Framework**: Streamlit
- **Telegram Bot Framework**: `python-telegram-bot` v20.7+ (Async)
- **AI Model**: Google Generative AI (`gemini-1.5-flash` / `google-genai`)
- **Audio Engine**: `gTTS` (Google Text-to-Speech)
- **Environment Management**: `python-dotenv`

---

## 📁 Repository Structure

```
RAKSHAK/
├── .env.example        # Environment variable template
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
├── config.py           # Configuration & Gemini system prompt template
├── detector.py         # Regex quick scanner & Gemini AI detector module
├── web_app.py          # Main Streamlit Web Application
├── bot.py              # Telegram Bot handlers & main polling client
├── test_detector.py    # Local test suite & validation script
└── README.md           # Documentation & deployment guide
```

---

## 🔑 Setup Guide

### Step 1: Obtain Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click **Get API Key** -> **Create API key in new project**.
4. Copy your key (starts with `AIzaSy...`).

### Step 2: Obtain Telegram Bot Token (Optional, for Telegram Bot)
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow instructions to get your HTTP Token.

---

## 💻 Local Installation & Execution

1. **Navigate to the repository:**
   ```bash
   cd /Users/rahulvoruganti/Desktop/RAKSHAK
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and insert your Gemini API Key:
   ```env
   GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
   TELEGRAM_BOT_TOKEN=7123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

5. **Run the Streamlit Web Application:**
   ```bash
   streamlit run web_app.py
   ```
   The web app will open automatically in your browser at `http://localhost:8501`.

6. **Run the Telegram Bot (Optional):**
   ```bash
   python bot.py
   ```

7. **Run Verification Test Suite:**
   ```bash
   python test_detector.py
   ```

---

## 🌐 Deploying on Streamlit Community Cloud (Free)

1. Push your repository to **GitHub** (ensure `.env` is listed in `.gitignore`).
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and log in with GitHub.
3. Click **New app** -> Select your `RAKSHAK` repository.
4. Set Main file path: `web_app.py`.
5. Click **Advanced settings...** -> **Secrets**:
   Add your Gemini API Key:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
6. Click **Deploy!** Your app will be live with a shareable URL.

---

## 🧪 Test Case Matrix

| Input Message | Expected Scam Detection | Primary Red Flags |
|---|---|---|
| `"Your Paytm KYC is pending. Update now: bit.ly/kyc"` | 🚨 Scam Detected (`KYC Scam`) | Urgent KYC threat, Phishing link |
| `"Congratulations! You won ₹10 Lakh in KBC. Send ₹5000 processing fee."` | 🚨 Scam Detected (`Lottery Scam`) | Lottery claim, Upfront fee demand |
| `"Hi, I sent ₹50,000 to you by mistake. Please return to 9876543210@upi"` | 🚨 Scam Detected (`Wrong Transfer Scam`) | Claim of accidental credit, Request to return money |
| `"Hello, how are you?"` | ✅ Safe (`None`) | Normal conversation |

---

## 🚨 Emergency Cybercrime Help

If you have fallen victim to financial cyber fraud in India:
- 📞 **Cybercrime Emergency Helpline**: Call **1930** immediately (Active 24x7)
- 🌐 **National Cyber Crime Reporting Portal**: [cybercrime.gov.in](https://cybercrime.gov.in)

---

## 📄 License
This project is licensed under the MIT License.
