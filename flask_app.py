"""
Rakshak - Flask Web Application & REST API Backend
"""

import logging
from flask import Flask, render_template, request, jsonify
from detector import detect_scam
from config import CYBERCRIME_HELPLINE, CYBERCRIME_PORTAL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RakshakFlask")

app = Flask(__name__)

@app.route("/")
def home():
    """Renders the main Rakshak HTML web application."""
    return render_template(
        "index.html",
        helpline=CYBERCRIME_HELPLINE,
        portal=CYBERCRIME_PORTAL
    )

@app.route("/api/analyze", methods=["POST"])
def analyze_message():
    """
    REST API Endpoint for Scam Analysis.
    Expects JSON body: {"message": "Suspicious text here"}
    Returns JSON analysis response.
    """
    try:
        data = request.get_json(force=True)
        message_text = data.get("message", "").strip() if data else ""

        if not message_text:
            return jsonify({
                "error": True,
                "message": "Message text is required."
            }), 400

        result = detect_scam(message_text)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Flask API Error: {e}")
        return jsonify({
            "error": True,
            "message": "An internal server error occurred while analyzing the message."
        }), 500

if __name__ == "__main__":
    print("🚀 Starting Rakshak Flask Web Server on http://127.0.0.1:5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
