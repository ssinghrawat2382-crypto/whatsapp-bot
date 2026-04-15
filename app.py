from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    msg = request.form.get("Body")

    reply = MessagingResponse()
    reply.message("You said: " + msg)

    return str(reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)