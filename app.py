from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

user_data = {}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body').strip().lower()
    sender = request.form.get('From')

    response = MessagingResponse()
    msg = response.message()

    # -------------------- START --------------------

    if incoming_msg in ['hi', 'hello', 'hey']:
        user_data[sender] = {"step": "ask_name"}

        msg.body(
            "👋 *Welcome to SmartBiz Automation*\n\n"
            "We help businesses handle customer queries automatically and never miss a lead.\n\n"
            "Let’s get started.\n\n"
            "👉 What’s your name?"
        )

    # -------------------- NAME CAPTURE --------------------

    elif sender in user_data and user_data[sender]["step"] == "ask_name":
        name = incoming_msg.capitalize()
        user_data[sender]["name"] = name
        user_data[sender]["step"] = "menu"

        # Save lead
        with open("leads.txt", "a") as f:
            f.write(f"{datetime.now()} | {sender} | {name}\n")

        msg.body(
            f"Great, *{name}!* 😊\n\n"
            "Here’s how we can help you:\n\n"
            "1️⃣ Explore Services\n"
            "2️⃣ View Pricing\n"
            "3️⃣ Book Appointment\n"
            "4️⃣ Talk to Expert\n"
            "5️⃣ Exit\n\n"
            "👉 Reply with a number to continue"
        )

    # -------------------- MENU --------------------

    elif sender in user_data and user_data[sender]["step"] == "menu":

        if incoming_msg == '1':
            msg.body(
                "💼 *Our Services*\n\n"
                "We provide:\n\n"
                "✔ WhatsApp Automation Setup\n"
                "✔ AI Chatbot Integration\n"
                "✔ Lead Capture Systems\n\n"
                "These help you respond instantly and increase conversions.\n\n"
                "👉 Type *menu* to go back"
            )

        elif incoming_msg == '2':
            msg.body(
                "💰 *Pricing Overview*\n\n"
                "🔹 Basic Setup: ₹999\n"
                "🔹 Advanced System: ₹1999\n\n"
                "Custom solutions available based on your needs.\n\n"
                "👉 Type *menu* to go back"
            )

        elif incoming_msg == '3':
            user_data[sender]["step"] = "appointment"
            msg.body(
                "📅 *Book an Appointment*\n\n"
                "Please share your preferred time.\n\n"
                "Examples:\n"
                "- Today 5pm\n"
                "- Tomorrow 11am\n\n"
                "We’ll confirm your slot shortly."
            )

        elif incoming_msg == '4':
            msg.body(
                "📞 *Talk to an Expert*\n\n"
                "You can directly connect with us:\n\n"
                "📱 WhatsApp/Call: 9XXXXXXXXX\n\n"
                "We usually respond within a few minutes."
            )

        elif incoming_msg == '5':
            msg.body(
                "👋 Thank you for visiting SmartBiz Automation.\n\n"
                "Feel free to message anytime.\n"
                "Have a great day!"
            )
            user_data.pop(sender, None)

        elif incoming_msg == 'menu':
            msg.body(
                "📋 *Main Menu*\n\n"
                "1️⃣ Explore Services\n"
                "2️⃣ View Pricing\n"
                "3️⃣ Book Appointment\n"
                "4️⃣ Talk to Expert\n"
                "5️⃣ Exit"
            )

        else:
            msg.body(
                "❌ Invalid input.\n\n"
                "Please select:\n"
                "1, 2, 3, 4 or 5\n\n"
                "Or type *menu*"
            )

    # -------------------- APPOINTMENT --------------------

    elif sender in user_data and user_data[sender]["step"] == "appointment":
        appointment_time = incoming_msg
        name = user_data[sender]["name"]

        # Save appointment
        with open("appointments.txt", "a") as f:
            f.write(f"{datetime.now()} | {sender} | {name} | {appointment_time}\n")

        msg.body(
            f"✅ *Appointment Request Submitted*\n\n"
            f"👤 Name: {name}\n"
            f"🕒 Preferred Time: {appointment_time}\n\n"
            "Our team will confirm shortly.\n\n"
            "👉 Type *menu* for more options"
        )

        user_data[sender]["step"] = "menu"

    # -------------------- FALLBACK --------------------

    else:
        msg.body(
            "👋 Hello!\n\n"
            "To begin, please type *hi*"
        )

    return str(response)

if __name__ == "__main__":
    app.run(port=5000)