from flask import Flask, request
import requests
import os
import psycopg2

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
DATABASE_URL = os.environ.get("DATABASE_URL")


# 🔹 Conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


# 🔹 Crear tablas si no existen
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            phone_number TEXT UNIQUE,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


create_tables()


# 🔹 Verificación del webhook
@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Error", 403


# 🔹 Recepción de mensajes
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry["changes"]:
                if change["value"].get("messages"):
                    message = change["value"]["messages"][0]
                    from_number = message["from"]
                    text = message["text"]["body"].lower()

                    save_user(from_number)

                    if text == "admin":
                        make_admin(from_number)
                        send_message(from_number, "Ahora eres administrador 🔐")

                    elif text.startswith("aviso "):
                        if is_admin(from_number):
                            aviso = text.replace("aviso ", "")
                            broadcast(aviso)
                            send_message(from_number, "Aviso enviado 📢")
                        else:
                            send_message(from_number, "No eres administrador ❌")

                    else:
                        send_message(from_number, "Comandos disponibles:\nadmin\naviso mensaje")

    return "ok", 200


# 🔹 Guardar usuario
def save_user(phone):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (phone_number) VALUES (%s) ON CONFLICT DO NOTHING;",
        (phone,)
    )
    conn.commit()
    cur.close()
    conn.close()


# 🔹 Convertir en admin
def make_admin(phone):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET is_admin = TRUE WHERE phone_number = %s;",
        (phone,)
    )
    conn.commit()
    cur.close()
    conn.close()


# 🔹 Verificar si es admin
def is_admin(phone):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT is_admin FROM users WHERE phone_number = %s;",
        (phone,)
    )
    result = cur.fetchone()
    cur.close()
    conn.close()

    return result and result[0]


# 🔹 Enviar aviso a todos
def broadcast(message):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT phone_number FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()

    for user in users:
        send_message(user[0], message)


# 🔹 Enviar mensaje WhatsApp
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
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

