import os
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN")  # توی Render باید اینو تو Environment بسازی
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# یک روت ساده برای تست
@app.route('/')
def home():
    return "ربات روشنه ✅"

# وقتی کاربر /start بزنه
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "سلام 👋 من ربات فراز گلد هستم")

# هر پیامی که فرستاده بشه
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"شما گفتید: {message.text}")

if __name__ == "__main__":
    # ربات روی webhook نمیاد چون روی Render فقط باید فلَسک روشن باشه
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
