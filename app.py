from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
import os
import google.generativeai as genai

app = Flask(__name__)

# =====================================================
# 🔐 GEMINI CONFIG
# =====================================================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# =====================================================
# 🧠 SIMPLE MEMORY (OPTIONAL)
# =====================================================
user_memory = {}

# =====================================================
# 🏠 HEALTH CHECK
# =====================================================
@app.route("/", methods=["GET"])
def home():
    return "Gemini SaaS Bot Running 🚀", 200

# =====================================================
# 🔗 WEBHOOK CHECK
# =====================================================
@app.route("/webhook", methods=["GET"])
def verify():
    return "Webhook Active ✅", 200

# =====================================================
# 🤖 GEMINI AI BRAIN
# =====================================================
def gemini_brain(user_msg, user_id):

    try:
        context = user_memory.get(user_id, "")

        prompt = f"""
You are a WhatsApp SaaS assistant for businesses.

Context:
{context}

User message:
{user_msg}

Rules:
- Give short, clear business answers
- Focus on automation, booking, pricing, support
"""

        response = model.generate_content(prompt)

        reply = response.text

        user_memory[user_id] = user_msg

        return reply

    except Exception as e:
        return "⚠️ AI temporarily unavailable"

# =====================================================
# 📩 WEBHOOK (SAAS + GEMINI)
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():

    if request.method != "POST":
        abort(405)

    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")

    response = MessagingResponse()
    msg = response.message()

    # -----------------------------
    # SYSTEM COMMANDS
    # -----------------------------
    if incoming_msg.lower() in ["hi", "hello", "start"]:
        msg.body(
            "👋 Welcome to Gemini SaaS Bot\n\n"
            "Ask anything like:\n"
            "• Build chatbot for clinic\n"
            "• Pricing system\n"
            "• Booking automation"
        )
        return str(response)

    if incoming_msg.lower() == "pricing":
        msg.body(
            "💰 Plans:\n\n"
            "Starter: ₹499/month\n"
            "Pro: ₹999/month\n"
            "Enterprise: ₹1999/month"
        )
        return str(response)

    # -----------------------------
    # 🧠 GEMINI AI RESPONSE
    # -----------------------------
    ai_reply = gemini_brain(incoming_msg, sender)

    msg.body(f"🤖 AI:\n\n{ai_reply}")

    return str(response)


# =====================================================
# 🚀 RUN SERVER
# =====================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)