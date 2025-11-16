from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend is running!", "message": "server is active"}), 200


@app.route("/send", methods=["POST", "OPTIONS"])
def send():
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200
    
    try:
        data = request.get_json()
        logger.info(f"Received data: {data}")
        
        if not data:
            return jsonify({"success": False, "message": "No data received"}), 400

        name = data.get("name")
        email = data.get("email")
        user_message = data.get("message")

        if not all([name, email, user_message]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        email_message = Message(
            subject=f"New contact from {name}",
            recipients=[os.getenv("MAIL_USERNAME")],
            body=f"Name: {name}\nEmail: {email}\nMessage: {user_message}"
        )

        mail.send(email_message)
        return jsonify({"success": True, "message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False)
