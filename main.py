from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = "YAHAN_APNA_NAYA_BOT_TOKEN_DALO"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Main Support Bot hoon.\n\n"
        "Commands:\n"
        "/help - Help\n"
        "/contact - Contact Support"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ Help:\n"
        "• Registration issue\n"
        "• Login issue\n"
        "• General support"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📩 Contact Support:\n"
        "@YourSupportUsername"
    )

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("contact", contact))

    print("Bot Started...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
