from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

# =====================================================
# 🏢 CLIENT CONFIG (EDIT ONLY THIS SECTION FOR CLIENTS)
# =====================================================

CLIENT = {
    "name": "Elite Automation Services",
    "industry": "Multi-Service Demo",
    "location": "Delhi, India",
    "contact": "+91-XXXXXXXXXX",
    "timings": "9AM - 9PM",
    "status": "active"
}

# =====================================================
# 🧠 UX MENU SYSTEM
# =====================================================

MENU = """
👋 Welcome to {name}

🏢 {industry}
📍 {location}

Choose an option:

1️⃣ Services
2️⃣ Pricing
3️⃣ Book / Order
4️⃣ Contact
5️⃣ About
6️⃣ Help Assistant
"""

# =====================================================
# 🏠 WEBHOOK HEALTH CHECK (RENDER VERIFICATION)
# =====================================================

@app.route("/", methods=["GET"])
def home():
    return f"{CLIENT['name']} WhatsApp Bot is LIVE 🚀", 200


# =====================================================
# 🔗 WEBHOOK VERIFICATION (OPTIONAL SAFETY CHECK)
# =====================================================

@app.route("/webhook", methods=["GET"])
def webhook_verify():
    """
    Optional verification endpoint
    Some platforms hit GET before POST
    """
    return "Webhook is active ✅", 200


# =====================================================
# 📩 MAIN WEBHOOK (TWILIO WHATSAPP ENTRY POINT)
# =====================================================

@app.route("/webhook", methods=["POST"])
def webhook():

    # -------------------------------
    # 1. VALIDATE REQUEST METHOD
    # -------------------------------
    if request.method != "POST":
        abort(405)

    # -------------------------------
    # 2. EXTRACT TWILIO DATA
    # -------------------------------
    incoming_msg = request.form.get("Body", "")
    sender = request.form.get("From", "")

    if not incoming_msg:
        incoming_msg = ""

    incoming_msg = incoming_msg.lower().strip()

    # -------------------------------
    # 3. RESPONSE OBJECT (TWILIO REQUIRED)
    # -------------------------------
    response = MessagingResponse()
    msg = response.message()

    # -------------------------------
    # 4. BOT LOGIC (UX FLOW)
    # -------------------------------

    # 🌟 Greeting
    if incoming_msg in ["hi", "hello", "hey", "start"]:
        msg.body(
            MENU.format(
                name=CLIENT["name"],
                industry=CLIENT["industry"],
                location=CLIENT["location"]
            )
        )

    # 🧾 Services
    elif incoming_msg in ["1", "services"]:
        msg.body(
            "🧾 Our Services:\n\n"
            "• Consultation\n"
            "• Customer Support Automation\n"
            "• Booking System\n"
            "• WhatsApp Automation Setup"
        )

    # 💰 Pricing
    elif incoming_msg in ["2", "pricing"]:
        msg.body(
            "💰 Pricing Plans:\n\n"
            "Basic: ₹499\n"
            "Standard: ₹999\n"
            "Premium: ₹1999\n\n"
            "📌 Contact for custom setup"
        )

    # 📅 Booking / Orders
    elif incoming_msg in ["3", "book", "order"]:
        msg.body(
            "📅 Booking Request Received!\n\n"
            "Send details:\n"
            "• Name\n"
            "• Service/Product\n"
            "• Time\n"
            "• Address\n\n"
            "We will confirm shortly ✅"
        )

    # 📞 Contact
    elif incoming_msg in ["4", "contact"]:
        msg.body(
            f"📞 Contact Info:\n\n"
            f"Phone: {CLIENT['contact']}\n"
            f"Location: {CLIENT['location']}\n"
            f"Timing: {CLIENT['timings']}"
        )

    # ℹ️ About
    elif incoming_msg in ["5", "about"]:
        msg.body(
            f"🏢 About {CLIENT['name']}:\n\n"
            "We provide automated WhatsApp customer handling systems "
            "for modern businesses."
        )

    # 🤖 Help Assistant Mode
    elif incoming_msg in ["6", "help", "assistant"]:
        msg.body(
            "🤖 Assistant Mode:\n\n"
            "Ask me anything like:\n"
            "• services\n"
            "• pricing\n"
            "• booking\n"
            "• contact\n\n"
            "I am here 24/7 🚀"
        )

    # ⏰ Time Utility
    elif "time" in incoming_msg:
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        msg.body(f"🕒 Server Time:\n{now}")

    # 🧠 Default fallback (important UX)
    else:
        msg.body(
            "🤖 Sorry, I didn’t understand that.\n\n"
            "Type 'hi' to see menu options."
        )

    # -------------------------------
    # 5. RETURN TWILIO RESPONSE (IMPORTANT WEBHOOK FORMALITY)
    # -------------------------------
    return str(response), 200


# =====================================================
# ⚠️ ERROR HANDLERS (PRODUCTION SAFETY)
# =====================================================

@app.errorhandler(404)
def not_found(e):
    return "Route not found", 404


@app.errorhandler(500)
def server_error(e):
    return "Internal server error", 500


# =====================================================
# 🚀 RUN SERVER (RENDER COMPATIBLE)
# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)