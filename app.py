from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import google.generativeai as genai
import traceback
import time

app = Flask(__name__)

# =========================
# GEMINI SETUP
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print("GEMINI INIT ERROR:", e)

# =========================
# MEMORY (simple)
# =========================
user_memory = {}

# =========================
# HOME
# =========================
@app.route("/", methods=["GET"])
def home():
    return "AI Bot Running 🚀", 200


# =========================
# SAFE GEMINI CALL (WITH TIME LIMIT)
# =========================
def gemini_reply(user_msg, sender):

    try:
        if model is None:
            return "⚠️ AI not configured"

        context = user_memory.get(sender, "")

        prompt = f"""
You are a WhatsApp assistant.

Context: {context}
User: {user_msg}

Reply short and helpful.
"""

        # ---- TIME SAFETY ----
        start = time.time()
        response = model.generate_content(prompt)

        if time.time() - start > 8:
            return "⚠️ AI timeout (too slow)"

        text = getattr(response, "text", None)

        if not text:
            return "⚠️ Empty AI response"

        user_memory[sender] = user_msg
        return text

    except Exception as e:
        print("AI ERROR:", e)
        return "⚠️ AI temporarily unavailable"


# =========================
# WEBHOOK (GUARANTEED RESPONSE)
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    resp = MessagingResponse()
    msg = resp.message()

    try:
        incoming = request.values.get("Body", "")
        sender = request.values.get("From", "")

        print("INCOMING:", sender, incoming)

        if not incoming:
            msg.body("⚠️ No message received")
            return str(resp)

        text = incoming.lower().strip()

        # ---------------- COMMANDS ----------------
        if text in ["hi", "hello", "start"]:
            msg.body("👋 Hello! Bot is active.")
            return str(resp)

        if text == "pricing":
            msg.body("💰 Plans:\nStarter ₹499\nPro ₹999\nEnterprise ₹1999")
            return str(resp)

        if text == "restart":
            user_memory[sender] = ""
            msg.body("🔄 Reset done")
            return str(resp)

        # ---------------- AI RESPONSE ----------------
        ai_text = gemini_reply(incoming, sender)

        # FINAL SAFETY FALLBACK
        if not ai_text:
            ai_text = "⚠️ Default fallback response"

        msg.body(f"🤖 {ai_text}")

        return str(resp)

    except Exception as e:
        print("WEBHOOK ERROR:", e)
        print(traceback.format_exc())

        # GUARANTEED RESPONSE (NEVER FAILS)
        msg.body("⚠️ Server error but bot is running")

        return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)