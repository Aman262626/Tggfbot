import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def get_reply(user_text):
    payload = {
        "message": user_text
    }

    try:
        r = requests.post(
            "https://ai-api-v71b.onrender.com/chat",
            json=payload,
            timeout=20
        )
        data = r.json()
        return data.get("response", "Hmm... mujhe samajh nahi aaya 🥺")
    except:
        return "Thoda sa error aa gaya baby 💔"


@app.route("/", methods=["GET"])
def home():
    return "Bot is running 💖"


@app.route("/", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    reply = get_reply(text)

    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": reply
        }
    )

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
