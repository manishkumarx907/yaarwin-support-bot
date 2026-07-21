import os
import logging
import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


# Gemini setup
genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello!\n\n"
        "Main AI Assistant Bot hu.\n"
        "Aap Hindi ya English me baat kar sakte ho.\n\n"
        "🤖 Ask me anything."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n\n"
        "/start - Start bot\n"
        "/help - Help\n\n"
        "Message bhejo aur AI reply karega."
    )


async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    try:
        response = model.generate_content(
            user_text
        )

        reply = response.text

        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(e)
        await update.message.reply_text(
            "❌ AI abhi available nahi hai. Thodi der baad try karo."
        )


def main():

    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_chat
        )
    )


    print("🤖 BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()


