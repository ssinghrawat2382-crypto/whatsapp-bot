from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
import os
import openai

app = Flask(__name__)

# =====================================================
# 🔐 OPENAI CONFIG (AI BRAIN)
# =====================================================
openai.api_key = os.getenv("OPENAI_API_KEY")  # set in Render

# =====================================================
# 🧠 SIMPLE SESSION MEMORY (OPTIONAL)
# =====================================================
user_memory = {}

# =====================================================
# 🏠 HEALTH CHECK
# =====================================================
@app.route("/", methods=["GET"])
def home():
    return "AI SaaS WhatsApp Bot Running 🚀", 200

# =====================================================
# 🔗 WEBHOOK VERIFICATION
# =====================================================
@app.route("/webhook", methods=["GET"])
def verify():
    return "Webhook Active ✅", 200

# =====================================================
# 🤖 AI BRAIN FUNCTION
# =====================================================
def ai_brain(user_msg, user_id):
    try:

        context = user_memory.get(user_id, "")

        prompt = f"""
You are a WhatsApp SaaS assistant for business automation.

Context:
{context}

User message:
{user_msg}

Rules:
- Be short and professional
- Focus on business automation (appointments, sales, support)
- Give structured replies
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a SaaS WhatsApp business assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response["choices"][0]["message"]["content"]

        # store context (light memory)
        user_memory[user_id] = user_msg

        return reply

    except Exception as e:
        return "⚠️ AI service temporarily unavailable. Please try again."

# =====================================================
# 📩 MAIN WEBHOOK (SAAS + AI HYBRID)
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():

    if request.method != "POST":
        abort(405)

    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")

    response = MessagingResponse()
    msg = response.message()

    # =================================================
    # 🟢 SYSTEM COMMANDS (CONTROL LAYER)
    # =================================================
    if incoming_msg.lower() in ["hi", "hello", "start"]:

        msg.body(
            "👋 Welcome to AI SaaS Assistant\n\n"
            "You can ask anything like:\n"
            "• I need a booking system\n"
            "• I want WhatsApp automation\n"
            "• Build chatbot for my clinic\n\n"
            "I will guide you automatically 🚀"
        )
        return str(response)

    if incoming_msg.lower() == "pricing":

        msg.body(
            "💰 SaaS Plans:\n\n"
            "Starter: ₹499/month\n"
            "Pro: ₹999/month\n"
            "Enterprise: ₹1999/month\n\n"
            "Reply 'help' for details"
        )
        return str(response)

    # =================================================
    # 🧠 AI BRAIN MODE (DEFAULT)
    # =================================================
    ai_reply = ai_brain(incoming_msg, sender)

    msg.body(f"🤖 AI Assistant:\n\n{ai_reply}")

    return str(response)


# =====================================================
# 🚀 RUN (RENDER READY)
# =====================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)