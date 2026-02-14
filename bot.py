from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

# 🔹 Verificación del webhook
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Error de verificación", 403


# 🔹 Recibir mensajes
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry["changes"]:
                if change["value"].get("messages"):
                    message = change["value"]["messages"][0]
                    from_number = message["from"]
                    text = message["text"]["body"]

                    print("Mensaje recibido:", text)

                    if text.lower() == "hola":
                        send_message(from_number, "Hola 👋 Bienvenida a mi bot 🚀")
                    else:
                        send_message(from_number, "No entendí tu mensaje 😅")

    return "ok", 200


# 🔹 Función para enviar mensaje
def send_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    requests.post(url, headers=headers, json=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
