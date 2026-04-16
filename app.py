from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

# =====================================================
# 🧠 SAAS DATABASE (SIMULATED - REPLACE WITH DB LATER)
# =====================================================

CLIENTS = {
    "default": {
        "name": "AI Automation Hub",
        "industry": "SaaS Demo",
        "location": "India",
        "contact": "+91-XXXXXXXXXX",
        "timings": "9AM - 9PM"
    },
    "clinic1": {
        "name": "City Health Clinic",
        "industry": "Healthcare",
        "location": "Delhi",
        "contact": "+91-1111111111",
        "timings": "24/7 Emergency"
    },
    "salon1": {
        "name": "Glow Beauty Salon",
        "industry": "Salon & Spa",
        "location": "Delhi",
        "contact": "+91-2222222222",
        "timings": "10AM - 9PM"
    }
}

# =====================================================
# 🧠 CLIENT DETECTION ENGINE (IMPORTANT SAAS LOGIC)
# =====================================================

def get_client(sender_number=None):
    """
    Future upgrade:
    - Map WhatsApp number → client_id
    - For now: default client
    """
    return CLIENTS["default"]

# =====================================================
# 🏠 HEALTH CHECK
# =====================================================

@app.route("/", methods=["GET"])
def home():
    return "SaaS WhatsApp System Running 🚀", 200

# =====================================================
# 🔗 WEBHOOK (TWILIO ENTRY POINT)
# =====================================================

@app.route("/webhook", methods=["POST"])
def webhook():

    if request.method != "POST":
        abort(405)

    incoming_msg = request.form.get("Body", "").lower().strip()
    sender = request.form.get("From", "")

    client = get_client(sender)

    response = MessagingResponse()
    msg = response.message()

    # =================================================
    # 🌟 SAAS GREETING (DYNAMIC CLIENT DATA)
    # =================================================

    if incoming_msg in ["hi", "hello", "hey", "start"]:
        msg.body(
            f"""👋 Welcome to {client['name']}

🏢 Industry: {client['industry']}
📍 Location: {client['location']}

Choose:
1️⃣ Services
2️⃣ Pricing
3️⃣ Contact
4️⃣ Help
"""
        )

    # =================================================
    # 🧾 SERVICES (GENERIC SAAS MODULE)
    # =================================================

    elif incoming_msg in ["1", "services"]:
        msg.body(
            "🧾 Services:\n\n"
            "• Customer Support Automation\n"
            "• Booking System\n"
            "• WhatsApp AI Replies\n"
            "• Lead Collection System"
        )

    # =================================================
    # 💰 PRICING (SAAS MONETIZATION CORE)
    # =================================================

    elif incoming_msg in ["2", "pricing"]:
        msg.body(
            "💰 Plans:\n\n"
            "Starter: ₹499/month\n"
            "Business: ₹999/month\n"
            "Pro: ₹1999/month\n\n"
            "📌 Upgrade anytime for more features"
        )

    # =================================================
    # 📞 CONTACT (DYNAMIC CLIENT DATA)
    # =================================================

    elif incoming_msg in ["3", "contact"]:
        msg.body(
            f"""📞 Contact Info:

Phone: {client['contact']}
Location: {client['location']}
Timing: {client['timings']}"""
        )

    # =================================================
    # 🤖 HELP / ASSISTANT MODE
    # =================================================

    elif incoming_msg in ["4", "help", "assistant"]:
        msg.body(
            "🤖 Assistant Mode:\n\n"
            "Ask anything like:\n"
            "• services\n"
            "• pricing\n"
            "• contact\n\n"
            "I work 24/7 🚀"
        )

    # =================================================
    # ⏰ UTILITY MODULE
    # =================================================

    elif "time" in incoming_msg:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg.body(f"🕒 Server Time:\n{now}")

    # =================================================
    # 🧠 FALLBACK AI STYLE RESPONSE
    # =================================================

    else:
        msg.body(
            "🤖 I didn’t understand that.\n\n"
            "Type 'hi' to see menu."
        )

    return str(response), 200


# =====================================================
# ⚠️ ERROR HANDLING (SAAS STABILITY)
# =====================================================

@app.errorhandler(404)
def not_found(e):
    return "Not Found", 404

@app.errorhandler(500)
def server_error(e):
    return "Server Error", 500


# =====================================================
# 🚀 RUN
# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)