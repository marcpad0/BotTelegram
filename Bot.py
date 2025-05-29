import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_HOST = os.environ["WEBHOOK_HOST"]  # e.g. https://my-app.onrender.com

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# WEBHOOK version
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),  # Render sets this
        webhook_url=f"{WEBHOOK_HOST}/webhook"
    )
