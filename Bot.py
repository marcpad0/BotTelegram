import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, AIORateLimiter

TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_HOST = os.environ["WEBHOOK_HOST"]  # es: https://nome-app.onrender.com

# Crea il bot
bot_app = Application.builder() \
    .token(TOKEN) \
    .rate_limiter(AIORateLimiter()) \
    .build()

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot attivo!")

bot_app.add_handler(CommandHandler("start", start))

# FastAPI app per ricevere webhook
api = FastAPI()

@api.on_event("startup")
async def startup():
    await bot_app.bot.set_webhook(url=f"{WEBHOOK_HOST}/webhook")

@api.get("/")
def root():
    return {"status": "ok"}

@api.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.update_queue.put(update)
    return {"ok": True}
