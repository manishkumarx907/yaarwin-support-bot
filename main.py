import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ======================
# CONFIG
# ======================

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_USERNAME = "@Vpnusern"
ADMIN_ID = 123456789   # यहां अपना numeric Telegram ID डालना


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# ======================
# START MENU
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("💰 Deposit", callback_data="deposit"),
            InlineKeyboardButton("💸 Withdrawal", callback_data="withdraw")
        ],
        [
            InlineKeyboardButton("🎁 Bonus", callback_data="bonus"),
            InlineKeyboardButton("💼 Daily Salary", callback_data="salary")
        ],
        [
            InlineKeyboardButton("👥 Referral", callback_data="referral")
        ],
        [
            InlineKeyboardButton("☎️ Customer Support", callback_data="support")
        ]
    ]

    reply = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Welcome to Virendra Support Bot\n\n"
        f"Please choose an option:",
        reply_markup=reply
    )


# ======================
# BUTTON HANDLER
# ======================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    responses = {

        "deposit":
        "💰 Deposit Support\n\nPlease contact support for deposit help.",

        "withdraw":
        "💸 Withdrawal Support\n\nPlease contact customer support.",

        "bonus":
        "🎁 Bonus information will be updated soon.",

        "salary":
        "💼 Daily Salary information will be updated soon.",

        "referral":
        "👥 Referral system information will be updated soon.",

        "support":
        "☎️ Please send your problem here.\nOur support team will reply."
    }


    await query.message.reply_text(
        responses.get(data, "Please try again.")
    )


# ======================
# USER MESSAGE TO ADMIN
# ======================

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    text = update.message.text


    if user.id != ADMIN_ID:

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "📩 New User Message\n\n"
                f"Name: {user.first_name}\n"
                f"Username: @{user.username}\n"
                f"ID: {user.id}\n\n"
                f"Message:\n{text}"
            )
        )


        await update.message.reply_text(
            "✅ Your message has been sent to support."
        )


    else:
        await update.message.reply_text(
            "Admin panel active."
        )



# ======================
# ERROR HANDLER
# ======================

async def error(update, context):

    logging.error(
        f"Error: {context.error}"
    )



# ======================
# RUN BOT
# ======================

def main():

    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    app.add_handler(
        CommandHandler("start", start)
    )


    app.add_handler(
        CallbackQueryHandler(buttons)
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            user_message
        )
    )


    app.add_error_handler(error)


    print("VIRENDRA BOT STARTED")

    app.run_polling()



if __name__ == "__main__":
    main()
