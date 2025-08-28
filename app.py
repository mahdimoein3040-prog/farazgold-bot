import os
import sys
import json
import logging
from typing import Any, Dict
from flask import Flask, request, jsonify
import requests

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("farazgold-bot")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "hook")
WEBHOOK_MODE = os.getenv("WEBHOOK_MODE", "true").lower() == "true"
PORT = int(os.getenv("PORT", "8000"))
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME") or os.getenv("HOSTNAME") or "localhost"

if not BOT_TOKEN:
    log.error("TELEGRAM_BOT_TOKEN is not set. Please set it as an environment variable.")

API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else None

app = Flask(__name__)

def tg_request(method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if not API:
        return {}
    try:
        r = requests.post(f"{API}/{method}", json=payload, timeout=20)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log.exception("Telegram request failed: %s", e)
        return {}

def send_message(chat_id: int, text: str, **kwargs):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    data.update(kwargs)
    return tg_request("sendMessage", data)

def set_webhook():
    if not API:
        return
    url = f"https://{HOSTNAME}/{WEBHOOK_SECRET}"
    try:
        tg_request("deleteWebhook", {"drop_pending_updates": False})
        res = tg_request("setWebhook", {"url": url, "allowed_updates": ["message"], "max_connections": 40})
        if res.get("ok"):
            log.info("Webhook set ✓ -> %s", url)
        else:
            log.warning("Failed to set webhook: %s", res)
    except Exception as e:
        log.exception("Error setting webhook: %s", e)

@app.get("/")
def health():
    return "OK", 200

@app.post(f"/{WEBHOOK_SECRET}")
def webhook():
    try:
        update = request.get_json(force=True, silent=True) or {}
        handle_update(update)
    except Exception as e:
        log.exception("Failed to handle update: %s", e)
    return jsonify({"ok": True})

def handle_update(update: Dict[str, Any]):
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if not chat_id or not text:
        return

    if text == "/start":
        send_message(chat_id, "سلام! 🤖\nمن آنلاینم. پیام بفرست تا جواب بدم.\n/ping برای تست")
        return

    if text == "/ping":
        send_message(chat_id, "pong ✅")
        return

    send_message(chat_id, f"دریافت شد:\n<code>{text}</code>")

if __name__ == "__main__":
    if WEBHOOK_MODE:
        log.info("Starting in WEBHOOK mode on port %s", PORT)
        if HOSTNAME and BOT_TOKEN:
            set_webhook()
        else:
            log.warning("HOSTNAME or BOT_TOKEN not available yet; webhook will be set later.")
        app.run(host="0.0.0.0", port=PORT)
    else:
        log.info("Starting in LONG-POLLING mode (local/dev). Flask will serve healthcheck on /")
        import threading, time
        def poll():
            if not API:
                log.error("Cannot start polling; TELEGRAM_BOT_TOKEN not set.")
                return
            log.info("Polling started.")
            offset = None
            while True:
                try:
                    r = requests.get(f"{API}/getUpdates", params={"timeout": 50, "offset": offset}, timeout=60)
                    r.raise_for_status()
                    data = r.json()
                    if data.get("ok"):
                        for upd in data.get("result", []):
                            offset = upd["update_id"] + 1
                            handle_update(upd)
                    else:
                        log.warning("getUpdates returned: %s", data)
                except Exception as e:
                    log.exception("Polling error: %s", e)
                    time.sleep(5)
        threading.Thread(target=poll, daemon=True).start()
        app.run(host="0.0.0.0", port=PORT)
