from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

# ----------------------------
# BUSINESS CONFIG (EDIT THIS)
# ----------------------------
BUSINESS_NAME = "My Business"
LOCATION = "Delhi, India"
OPENING_HOURS = "9:00 AM - 9:00 PM"

PRODUCTS = {
    "milk": "Fresh Milk - ₹60/Litre",
    "bread": "Brown Bread - ₹40",
    "eggs": "Eggs - ₹6 per piece",
    "rice": "Basmati Rice - ₹80/kg"
}

# ----------------------------
# WEBHOOK HEALTH CHECK (RENDER)
# ----------------------------
@app.route("/", methods=["GET"])
def home():
    return f"{BUSINESS_NAME} WhatsApp Bot is LIVE 🚀", 200


# ----------------------------
# WEBHOOK ENDPOINT (TWILIO)
# ----------------------------
@app.route("/webhook", methods=["POST"])
def webhook():

    # ----------------------------
    # 1. VALIDATE REQUEST (FORMALITY)
    # ----------------------------
    if request.method != "POST":
        abort(405)

    # Twilio sends data in FORM format
    incoming_msg = request.form.get("Body")
    sender = request.form.get("From")

    # Safety check (avoid crashes)
    if not incoming_msg:
        incoming_msg = ""

    incoming_msg = incoming_msg.lower().strip()

    # ----------------------------
    # 2. TWILIO RESPONSE OBJECT
    # ----------------------------
    response = MessagingResponse()
    msg = response.message()

    # ----------------------------
    # 3. BOT LOGIC
    # ----------------------------

    # Greeting
    if incoming_msg in ["hi", "hello", "hey"]:
        msg.body(
            f"👋 Welcome to {BUSINESS_NAME}\n\n"
            "Options:\n"
            "1️⃣ Products\n"
            "2️⃣ Prices\n"
            "3️⃣ Location\n"
            "4️⃣ Timings\n"
            "5️⃣ Contact"
        )

    # Products
    elif incoming_msg in ["1", "product", "products"]:
        product_text = "\n".join([f"• {k.title()} - {v}" for k, v in PRODUCTS.items()])
        msg.body(f"🛒 Products:\n\n{product_text}")

    # Prices
    elif incoming_msg in ["2", "price", "prices"]:
        price_text = "\n".join([f"• {k.title()} - {v}" for k, v in PRODUCTS.items()])
        msg.body(f"💰 Price List:\n\n{price_text}")

    # Location
    elif incoming_msg in ["3", "location"]:
        msg.body(f"📍 Location:\n{LOCATION}")

    # Timings
    elif incoming_msg in ["4", "time", "timings"]:
        msg.body(f"⏰ Opening Hours:\n{OPENING_HOURS}")

    # Contact
    elif incoming_msg in ["5", "contact"]:
        msg.body(
            "📞 Contact Details:\n"
            "Phone: +91-XXXXXXXXXX\n"
            "Email: support@business.com"
        )

    # Order flow
    elif "order" in incoming_msg or "book" in incoming_msg:
        msg.body(
            "🛒 Order Received!\n\n"
            "Please send:\n"
            "• Product name\n"
            "• Quantity\n"
            "• Address\n\n"
            "Our team will confirm shortly ✅"
        )

    # Time check
    elif "time now" in incoming_msg:
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        msg.body(f"🕒 Server Time:\n{now}")

    # Default response
    else:
        msg.body(
            "🤖 Sorry, I didn’t understand.\n\n"
            "Type 'hi' for options."
        )

    # ----------------------------
    # 4. RETURN TWILIO XML RESPONSE
    # ----------------------------
    return str(response), 200


# ----------------------------
# 5. ERROR HANDLER (WEBHOOK SAFETY)
# ----------------------------
@app.errorhandler(404)
def not_found(e):
    return "Route not found", 404


@app.errorhandler(500)
def server_error(e):
    return "Server error", 500


# ----------------------------
# 6. RUN (RENDER COMPATIBLE)
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)