from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# ----------------------------
# MAIN ROUTE (HOME CHECK)
# ----------------------------
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is Running 🚀", 200


# ----------------------------
# WHATSAPP WEBHOOK ROUTE
# ----------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Get incoming message from WhatsApp
        incoming_msg = request.form.get("Body")
        sender = request.form.get("From")

        # Create Twilio response object
        response = MessagingResponse()
        msg = response.message()

        # Normalize input
        if incoming_msg:
            incoming_msg = incoming_msg.lower().strip()
        else:
            incoming_msg = ""

        # ----------------------------
        # SIMPLE BOT LOGIC
        # ----------------------------

        if incoming_msg in ["hi", "hello", "hey"]:
            msg.body("Hello 👋 I am your WhatsApp bot. How can I help you?")
        
        elif "help" in incoming_msg:
            msg.body("You can ask me anything. Example: hi, time, or info")

        elif "time" in incoming_msg:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg.body(f"Current server time is:\n{current_time}")

        elif "nursing" in incoming_msg:
            msg.body("You are a Nursing student 👨‍⚕️📚 Keep going strong!")

        elif incoming_msg == "":
            msg.body("I didn't receive any message. Please send again.")

        else:
            msg.body(f"You said: {incoming_msg}\n\nI am still learning 🤖")

        return str(response)

    except Exception as e:
        # Error handling (important for production)
        response = MessagingResponse()
        response.message("Bot error occurred ⚠️ Please try again later.")
        return str(response)


# ----------------------------
# RUN APP (IMPORTANT FOR RENDER)
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)