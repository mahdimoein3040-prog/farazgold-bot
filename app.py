import os
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/')
def home():
    return "FarazGold Bot is running!"

@app.route('/signal', methods=['POST'])
def signal():
    data = request.json
    message = data.get("message", "No signal provided.")
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    return {"status": "ok", "message": message}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
