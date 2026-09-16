import os

from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
)

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app_web = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context):
    await update.message.reply_text(
        "Bot aktif!\n\n"
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/id - Lihat ID Telegram\n"
        "/ping - Cek bot"
    )


async def help_command(update: Update, context):
    await update.message.reply_text(
        "Bot siap digunakan.\n\n"
        "/start\n"
        "/help\n"
        "/id\n"
        "/ping"
    )


async def get_id(update: Update, context):
    await update.message.reply_text(
        f"Telegram ID lo: {update.effective_user.id}"
    )


async def ping(update: Update, context):
    await update.message.reply_text("Pong! Bot aktif.")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("id", get_id))
telegram_app.add_handler(CommandHandler("ping", ping))


@app_web.route("/", methods=["GET"])
def home():
    return "Bot Telegram aktif!"


@app_web.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, telegram_app.bot)

    await telegram_app.process_update(update)

    return "OK"


@app_web.route("/health", methods=["GET"])
def health():
    return "OK"


async def setup():
    await telegram_app.initialize()

    if WEBHOOK_URL:
        await telegram_app.bot.set_webhook(
            url=f"{WEBHOOK_URL}/webhook"
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(setup())

    app_web.run(
        host="0.0.0.0",
        port=PORT
    )
