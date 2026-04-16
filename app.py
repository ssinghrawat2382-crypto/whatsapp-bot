from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# =====================================================
# 🧠 USER SESSION STATE (SIMPLE SAAS DEMO MEMORY)
# =====================================================
user_state = {}

# =====================================================
# 🏢 CLIENT CONFIG (FOR DEMO PURPOSE)
# =====================================================
CLIENT = {
    "name": "AI Automation SaaS Demo",
    "contact": "+91-XXXXXXXXXX",
    "location": "India"
}

# =====================================================
# 🏠 HEALTH CHECK (RENDER VERIFICATION)
# =====================================================
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp SaaS Bot Running 🚀", 200


# =====================================================
# 🔗 WEBHOOK VERIFICATION (TWILIO SAFETY)
# =====================================================
@app.route("/webhook", methods=["GET"])
def webhook_verify():
    """
    Twilio or browsers may hit GET request first
    """
    return "Webhook Active ✅", 200


# =====================================================
# 📩 MAIN WHATSAPP WEBHOOK (PRODUCTION CORE)
# =====================================================
@app.route("/webhook", methods=["POST"])
def webhook():

    # -----------------------------
    # 1. METHOD VALIDATION
    # -----------------------------
    if request.method != "POST":
        abort(405)

    # -----------------------------
    # 2. EXTRACT DATA SAFELY
    # -----------------------------
    incoming_msg = request.form.get("Body", "").lower().strip()
    sender = request.form.get("From", "")

    # -----------------------------
    # 3. INIT RESPONSE
    # -----------------------------
    response = MessagingResponse()
    msg = response.message()

    # -----------------------------
    # 4. GET USER STATE
    # -----------------------------
    state = user_state.get(sender, 0)

    # =====================================================
    # 🟢 STEP 0 → WELCOME SCREEN
    # =====================================================
    if state == 0:
        msg.body(
            "👋 Welcome to AI SaaS Demo Bot\n\n"
            "Choose your business type:\n"
            "1️⃣ Clinic\n"
            "2️⃣ Salon\n"
            "3️⃣ Pharmacy\n\n"
            "Reply with option number"
        )
        user_state[sender] = 1


    # =====================================================
    # 🟡 STEP 1 → INDUSTRY SELECTION
    # =====================================================
    elif state == 1:

        if incoming_msg == "1":
            msg.body("🏥 Clinic selected\n\nReply YES to continue demo")
            user_state[sender] = 2

        elif incoming_msg == "2":
            msg.body("💇 Salon selected\n\nReply YES to continue demo")
            user_state[sender] = 2

        elif incoming_msg == "3":
            msg.body("💊 Pharmacy selected\n\nReply YES to continue demo")
            user_state[sender] = 2

        else:
            msg.body("❌ Invalid option. Please choose 1, 2 or 3.")


    # =====================================================
    # 🔵 STEP 2 → CONFIRMATION
    # =====================================================
    elif state == 2:

        if incoming_msg == "yes":
            msg.body(
                "⚡ Smart Automation Features:\n\n"
                "✔ Auto replies\n"
                "✔ Booking system\n"
                "✔ Customer handling\n\n"
                "Reply YES to continue"
            )
            user_state[sender] = 3
        else:
            msg.body("Please reply YES to continue demo")


    # =====================================================
    # 🟣 STEP 3 → BENEFITS
    # =====================================================
    elif state == 3:

        if incoming_msg == "yes":
            msg.body(
                "🚀 Business Benefits:\n\n"
                "✔ 24/7 automation\n"
                "✔ No missed customers\n"
                "✔ Faster response time\n\n"
                "Reply YES for pricing"
            )
            user_state[sender] = 4
        else:
            msg.body("Reply YES to continue")


    # =====================================================
    # 🟠 STEP 4 → PRICING
    # =====================================================
    elif state == 4:

        if incoming_msg == "yes":
            msg.body(
                "💰 Pricing Plans:\n\n"
                "Starter: ₹499/month\n"
                "Pro: ₹999/month\n"
                "Business: ₹1999/month\n\n"
                "Reply YES for contact details"
            )
            user_state[sender] = 5
        else:
            msg.body("Reply YES to view pricing")


    # =====================================================
    # 🔴 STEP 5 → CONTACT
    # =====================================================
    elif state == 5:

        if incoming_msg == "yes":
            msg.body(
                f"📞 Contact Sales:\n\n"
                f"{CLIENT['contact']}\n\n"
                "Demo completed ✅\n"
                "Type RESTART to try again"
            )
            user_state[sender] = 6
        else:
            msg.body("Reply YES for contact details")


    # =====================================================
    # ⚫ STEP 6 → END / RESET FLOW
    # =====================================================
    elif state == 6:

        if incoming_msg == "restart":
            user_state[sender] = 0
            msg.body("🔄 Restarting demo...\nSend hi to begin again")
        else:
            msg.body("Demo completed. Type RESTART to start again")


    # =====================================================
    # 🧠 GLOBAL FALLBACK (SAFETY LAYER)
    # =====================================================
    else:
        user_state[sender] = 0
        msg.body("👋 Send 'hi' to start demo again")


    # -----------------------------
    # 5. RETURN TWILIO RESPONSE
    # -----------------------------
    return str(response), 200


# =====================================================
# 🚀 RUN SERVER (RENDER READY)
# =====================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)