from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Home route (to check if server is running)
@app.route("/")
def home():
    return "Bot is running successfully"

# WhatsApp webhook (main chatbot logic)
@app.route("/webhook", methods=["POST"])
def webhook():
    # Get message from WhatsApp user
    incoming_msg = request.form.get("Body")

    # Debug log (check in Render logs)
    print("MESSAGE RECEIVED:", incoming_msg)

    # Create Twilio response
    response = MessagingResponse()
    msg = response.message()

    # Reply back to user
    msg.body("You said: " + str(incoming_msg))

    return str(response)

# Run app (important for deployment)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)