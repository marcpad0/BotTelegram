import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import AIORateLimiter
from telegram.ext.webhook import WebhookUpdate

TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_HOST = os.environ["WEBHOOK_HOST"]  # es: https://tuo-bot.onrender.com

app = Application.builder() \
    .token(TOKEN) \
    .rate_limiter(AIORateLimiter()) \
    .build()

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Il bot è online 🚀")

app.add_handler(CommandHandler("start", start))

# FastAPI per ricevere i webhook
api = FastAPI()

@api.get("/")
def home():
    return {"status": "ok"}

@api.post("/webhook")
async def process_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(WebhookUpdate(update))
    return {"ok": True}

@app.on_startup
async def on_startup():
    await app.bot.set_webhook(url=f"{WEBHOOK_HOST}/webhook")
