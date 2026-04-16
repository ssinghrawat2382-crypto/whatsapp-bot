from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
import os
import google.generativeai as genai

app = Flask(__name__)

# =====================================================
# 🔐 GEMINI CONFIG
# =====================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# =====================================================
# 🧠 SIMPLE MEMORY (SAFE)
# =====================================================
user_memory = {}

# =====================================================
# 🏠 HEALTH CHECK
# =====================================================
@app.route("/", methods=["GET"])
def home():
    return "AI SaaS Bot Running 🚀", 200

# =====================================================
# 🔗 WEBHOOK TEST
# =====================================================
@app.route("/webhook", methods=["GET"])
def webhook_test():
    return "Webhook Active ✅", 200

# =====================================================
# 🧠 GEMINI AI FUNCTION (SAFE + CONTROLLED)
# =====================================================
def gemini_reply(user_msg, sender):

    try:
        if not GEMINI_API_KEY:
            return "⚠️ AI not configured (missing GEMINI_API_KEY)"

        context = user_memory.get(sender, "")

        prompt = f"""
You are a WhatsApp SaaS assistant.

Context: {context}

User message: {user_msg}

Rules:
- Keep answers short
- Focus on business (booking, pricing, automation)
"""

        response = model.generate_content(prompt)

        reply = response.text if response and response.text else "⚠️ No response from AI"

        user_memory[sender] = user_msg

        return reply

    except Exception as e:
        print("AI ERROR:", str(e))  # IMPORTANT FOR RENDER DEBUG
        return "⚠️ AI service temporarily unavailable"


# =====================================================
# 📩 MAIN WEBHOOK (ROBUST VERSION)
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():

    try:
        # -----------------------------
        # SAFE DATA EXTRACTION
        # -----------------------------
        incoming_msg = request.form.get("Body", "")
        sender = request.form.get("From", "")

        print("Incoming:", sender, incoming_msg)  # DEBUG LOG

        # -----------------------------
        # RESPONSE OBJECT
        # -----------------------------
        response = MessagingResponse()
        msg = response.message()

        if not incoming_msg:
            msg.body("⚠️ Empty message received")
            return str(response)

        text = incoming_msg.lower().strip()

        # -----------------------------
        # SYSTEM COMMANDS
        # -----------------------------
        if text in ["hi", "hello", "start"]:

            msg.body(
                "👋 Welcome to AI SaaS Bot\n\n"
                "You can ask:\n"
                "• Build chatbot\n"
                "• Pricing\n"
                "• Automation help"
            )
            return str(response)

        if text == "pricing":

            msg.body(
                "💰 Plans:\n\n"
                "Starter: ₹499/month\n"
                "Pro: ₹999/month\n"
                "Enterprise: ₹1999/month"
            )
            return str(response)

        if text == "restart":
            user_memory[sender] = ""
            msg.body("🔄 Reset done. Send hi to start again.")
            return str(response)

        # -----------------------------
        # 🧠 AI BRAIN RESPONSE
        # -----------------------------
        ai_text = gemini_reply(incoming_msg, sender)

        msg.body(f"🤖 AI:\n\n{ai_text}")

        return str(response)

    except Exception as e:
        print("WEBHOOK ERROR:", str(e))  # CRITICAL LOGGING

        response = MessagingResponse()
        response.message("⚠️ Server error. Try again later.")

        return str(response)


# =====================================================
# 🚀 RUN APP
# =====================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)