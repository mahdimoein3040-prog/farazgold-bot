from fastapi import FastAPI
import requests
import yaml
import os

app = FastAPI()

# بارگذاری تنظیمات از config.yaml
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

TELEGRAM_TOKEN = config["telegram"]["token"]
CHAT_ID = config["telegram"]["chat_id"]
TARGET_URL = config["scraper"]["url"]

@app.get("/")
def home():
    return {"message": "FarazGold bot is running!"}

@app.get("/price")
def get_price():
    try:
        response = requests.get(TARGET_URL, timeout=10)
        response.raise_for_status()
        return {"price": "123456"}  # اینجا بعداً میشه real scraper
    except Exception as e:
        return {"error": str(e)}
