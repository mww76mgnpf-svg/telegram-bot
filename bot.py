import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot aktif!\n\n"
        "/start - Mulai bot\n"
        "/help - Bantuan\n"
        "/id - Lihat ID Telegram\n"
        "/ping - Cek bot"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot siap digunakan.\n\n"
        "/start\n"
        "/help\n"
        "/id\n"
        "/ping"
    )

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Telegram ID lo: {update.effective_user.id}"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! Bot aktif.")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN belum dipasang.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("ping", ping))

    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
