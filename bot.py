"""
Rakshak - Telegram Bot Main Entrypoint
Telegram Bot for Indian UPI Scam Detection using Google Gemini 1.5 Flash AI
"""

import logging
import asyncio
from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from config import TELEGRAM_BOT_TOKEN, CYBERCRIME_HELPLINE, CYBERCRIME_PORTAL
from detector import detect_scam

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("RakshakBot")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    welcome_text = (
        "🛡️ *Welcome to Rakshak (रक्षक) - AI UPI Scam Detector!*\n\n"
        "India loses over ₹1000+ Crore annually to financial scams. "
        "Rakshak uses Google Gemini AI to analyze suspicious messages and protect you from fraudulent links, "
        "fake lottery claims, KYC block threats, and UPI payment traps.\n\n"
        "📱 *How to Use Rakshak:*\n"
        "• *Forward or paste* any SMS, WhatsApp message, or email text directly into this chat.\n"
        "• Rakshak will instantly scan for red flags and tell you if it's safe or a scam.\n\n"
        "📌 *Available Commands:*\n"
        "• `/start` - Restart the bot & view intro\n"
        "• `/help` - View usage guide & sample scams\n"
        "• `/about` - Learn about Rakshak & Indian UPI security\n"
        "• `/report` - Get Cybercrime Helpline (1930) details\n\n"
        "🚨 *Lost money to cyber fraud? Call 1930 immediately!*"
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command."""
    help_text = (
        "🔍 *Rakshak Scam Detection Guide*\n\n"
        "Rakshak identifies the following major Indian fraud patterns:\n"
        "1️⃣ *KYC Update Scam*: Fake threats to block Paytm, SBI, or SIM cards.\n"
        "2️⃣ *Lottery / KBC Scam*: Fake announcements of winning ₹10 Lakhs or cars.\n"
        "3️⃣ *Wrong Transfer Scam*: Pretending to accidentally send money to your UPI.\n"
        "4️⃣ *Phishing Links*: Fake bank update links or APK download requests.\n"
        "5️⃣ *Fake UPI / PIN Scam*: Asking you to enter UPI PIN to *receive* money.\n"
        "6️⃣ *Part-time Job Scam*: YouTube like/comment jobs demanding fees.\n"
        "7️⃣ *Instant Loan Scam*: Loans requiring advance processing fees.\n\n"
        "🧪 *Test Examples to Copy & Paste:* \n"
        "• `Your Paytm KYC is pending. Update now: bit.ly/kyc`\n"
        "• `Congratulations! You won ₹10 Lakh in KBC. Send ₹5000 processing fee.`\n"
        "• `I sent ₹50,000 to you by mistake. Please return to 9876543210@upi`\n\n"
        "💡 *Golden Rule of UPI:* UPI PIN is ONLY needed to SEND money, never to RECEIVE money!"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /about command."""
    about_text = (
        "ℹ️ *About Rakshak (रक्षक)*\n\n"
        "*Mission:* Protecting 500 Million+ Indian UPI users from financial cyber fraud.\n"
        "*AI Engine:* Powered by Google Gemini 1.5 Flash & Regex Quick-Scan engine.\n"
        "*Target Frauds:* Smishing, Phishing, UPI Pin traps, KYC blocking, Fake Lottery, Remote Screen Sharing scams.\n\n"
        "📊 *Cybercrime Insight:* Over 70% of digital payment victims fall for fake urgency in SMS/WhatsApp messages. "
        "Rakshak acts as your personal AI shield before you make a wrong payment click.\n\n"
        "🇮🇳 *Stay Safe. Stay Alert.*"
    )
    await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /report command."""
    report_text = (
        "🚨 *National Cyber Crime Reporting Helpline*\n\n"
        "If you or someone you know has lost money to a digital fraud:\n\n"
        f"📞 *Call Emergency Helpline:* `{CYBERCRIME_HELPLINE}` (Toll-Free, 24x7)\n"
        f"🌐 *Official Reporting Portal:* {CYBERCRIME_PORTAL}\n\n"
        "⚡ *Immediate Action Steps:* \n"
        "1. Call 1930 within the first 1-2 hours (Golden Hours) to block payment transfer.\n"
        "2. Report the incident at cybercrime.gov.in.\n"
        "3. Notify your bank to temporarily freeze your UPI/NetBanking credentials.\n"
        "4. Save screenshots of fraud SMS, WhatsApp chats, and UPI transaction reference IDs."
    )
    await update.message.reply_text(report_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

def format_detection_response(res: dict) -> str:
    """Formats the AI analysis dictionary into Telegram Markdown message."""
    is_scam = res.get("is_scam", False)
    risk_score = res.get("risk_score", "Medium")
    scam_type = res.get("scam_type", "Unknown Scam")
    red_flags = res.get("red_flags", [])
    explanation = res.get("explanation", "No detailed explanation provided.")
    action = res.get("action", "Stay cautious.")
    hindi_warning = res.get("hindi_warning", "")

    # Risk badge mapping
    risk_badges = {
        "Low": "🟢 Low",
        "Medium": "🟡 Medium",
        "High": "🟠 High",
        "Critical": "🔴 CRITICAL"
    }
    risk_badge = risk_badges.get(risk_score, "🟡 " + risk_score)

    if is_scam:
        msg = f"🚨 *SCAM DETECTED!*\n\n"
        msg += f"🔥 *Risk Level:* {risk_badge}\n"
        msg += f"🏷️ *Scam Type:* `{scam_type}`\n\n"

        if red_flags:
            msg += "⚠️ *Red Flags Found:*\n"
            for flag in red_flags:
                msg += f"• {flag}\n"
            msg += "\n"

        msg += f"📖 *Explanation:* {explanation}\n\n"
        msg += f"✅ *What to do:* {action}\n\n"

        if hindi_warning:
            msg += f"🔊 *Hindi Warning:* _{hindi_warning}_\n\n"

        msg += "---\n"
        msg += f"🚨 *Lost money? Call 1930 immediately or report on cybercrime.gov.in!*"
    else:
        msg = f"✅ *Message appears SAFE*\n\n"
        msg += f"📊 *Risk Score:* {risk_badge}\n"
        msg += f"📖 *Analysis:* {explanation}\n\n"
        msg += f"💡 *Advice:* {action}\n\n"
        msg += "---\n"
        msg += "🤔 *Still not sure?* Forward to a family member or friend before taking action."

    return msg

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming text messages, runs quick scan and AI scam analysis."""
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()
    
    # Send typing action to user while processing
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    try:
        # Run scam detection
        result = detect_scam(user_text)
        formatted_response = format_detection_response(result)

        await update.message.reply_text(
            formatted_response,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Error processing message from user {update.effective_user.id}: {e}")
        error_reply = (
            "⚠️ *An error occurred while analyzing the message.*\n\n"
            "Please try sending the message again. Remember: Never share OTPs or enter your UPI PIN to receive money."
        )
        await update.message.reply_text(error_reply, parse_mode=ParseMode.MARKDOWN)

def main():
    """Starts the Telegram bot client."""
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
        print("❌ ERROR: TELEGRAM_BOT_TOKEN is not configured in .env file!")
        print("Please set TELEGRAM_BOT_TOKEN in .env and restart the bot.")
        return

    print("🚀 Starting Rakshak Telegram Bot...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add Command Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("report", report_command))

    # Add Message Handler for scam analysis
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Start Polling
    print("✅ Rakshak Bot is live and listening for messages!")
    app.run_polling()

if __name__ == "__main__":
    main()
