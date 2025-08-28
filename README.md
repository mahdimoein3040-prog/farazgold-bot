# farazgold-bot (Render + Telegram Webhook)

A tiny Python/Flask Telegram bot prepared for Render. Uses webhook by default.

## Files
- `app.py` — Flask app + Telegram webhook handler
- `requirements.txt` — Python dependencies
- `Procfile` — how to start the app on Render
- `render.yaml` — optional blueprint for Render
- `README.md` — this file

## Local run
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
$env:WEBHOOK_MODE="false"   # use long polling locally
python app.py
```

## Deploy to Render (Web Service)
1. Push these files to a GitHub repo (e.g., `farazgold-bot`).
2. In Render: **New → Web Service → Public Git Repository**, paste your repo URL.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --preload --workers=1 --threads=4 --timeout=120`
5. Set Environment Variables:
   - `TELEGRAM_BOT_TOKEN` = your bot token
   - `WEBHOOK_MODE` = `true` (default)
   - `WEBHOOK_SECRET` = any random string (e.g. a GUID)
6. Deploy. When it's live, logs should show **"Webhook set ✓"**.
7. Message your bot on Telegram to test.

> Never commit your real token to Git! Use Render's Environment Variables.
