import os
import sqlite3
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from openai import OpenAI


BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

ADMIN_ID = 7871103989

client = OpenAI(api_key=OPENAI_KEY)


logging.basicConfig(
    level=logging.INFO
)


# ================= DATABASE =================

db = sqlite3.connect("users.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
name TEXT,
registered INTEGER DEFAULT 0
)
""")

db.commit()



def save_user(user):

    cursor.execute(
        "INSERT OR IGNORE INTO users(id,username,name) VALUES(?,?,?)",
        (
            user.id,
            user.username,
            user.first_name
        )
    )

    db.commit()



# ================= START =================


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    save_user(user)


    keyboard = [

        [
            InlineKeyboardButton(
                "🟢 Register Now",
                url="https://www.yaarwin.online/#/register?invitationCode=182763900728"
            )
        ],

        [
            InlineKeyboardButton(
                "✅ I Have Registered",
                callback_data="registered"
            )
        ],

        [
            InlineKeyboardButton(
                "🤖 AI Support",
                callback_data="ai"
            )
        ]

    ]


    await update.message.reply_text(
        "👋 Welcome to Virendra Support Bot\n\n"
        "Please choose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
# ================= BUTTONS =================


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id


    if query.data == "registered":

        cursor.execute(
            "UPDATE users SET registered=1 WHERE id=?",
            (user_id,)
        )

        db.commit()


        keyboard = [

            [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
            [InlineKeyboardButton("💸 Withdrawal", callback_data="withdraw")],

            [InlineKeyboardButton("🎁 Bonus", callback_data="bonus")],
            [InlineKeyboardButton("💼 Daily Salary", callback_data="salary")],

            [InlineKeyboardButton("👥 Referral", callback_data="referral")],

            [InlineKeyboardButton("📞 Customer Support", callback_data="support")],

            [InlineKeyboardButton("❓ FAQ", callback_data="faq")]

        ]


        await query.edit_message_text(
            "✅ Registration Completed!\n\nChoose your option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )



    elif query.data == "deposit":

        await query.message.reply_text(
            "💰 Deposit Support\n\n"
            "For deposit related help contact support."
        )


    elif query.data == "withdraw":

        await query.message.reply_text(
            "💸 Withdrawal Support\n\n"
            "Please send your issue to support."
        )


    elif query.data == "bonus":

        await query.message.reply_text(
            "🎁 Bonus information will be updated soon."
        )


    elif query.data == "salary":

        await query.message.reply_text(
            "💼 Daily Salary information will be updated soon."
        )


    elif query.data == "referral":

        await query.message.reply_text(
            "👥 Referral system information will be updated soon."
        )


    elif query.data == "faq":

        await query.message.reply_text(
            "❓ FAQ\n\n"
            "• How to register?\n"
            "Use Register button.\n\n"
            "• Need help?\n"
            "Contact support."
        )


    elif query.data == "support":

        await query.message.reply_text(
            "📞 Please type your problem.\n"
            "Support team will receive it."
        )



# ================= USER MESSAGE TO ADMIN =================


async def user_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    text = update.message.text


    if user.id == ADMIN_ID:
        return


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



# ================= ADMIN REPLY =================


async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return


    if len(context.args) < 2:

        await update.message.reply_text(
            "Use:\n/reply user_id message"
        )

        return


    user_id = context.args[0]

    message = " ".join(context.args[1:])


    await context.bot.send_message(
        chat_id=int(user_id),
        text=(
            "📞 Support Reply:\n\n"
            + message
        )
    )
# ================= AI CHAT =================


async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text


    # Admin ke messages ko AI par nahi bhejna
    if update.message.from_user.id == ADMIN_ID:
        return


    try:

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are Virendra Support Bot. "
                    "Reply like a real human support agent. "
                    "Understand Hindi and English. "
                    "Be polite and helpful."
                },

                {
                    "role": "user",
                    "content": user_text
                }

            ]

        )


        answer = response.choices[0].message.content


        await update.message.reply_text(answer)


    except Exception as e:

        logging.error(e)

        await update.message.reply_text(
            "Sorry, I am unable to reply right now. Please try again."
        )



# ================= ADMIN COMMANDS =================


async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return


    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    count = cursor.fetchone()[0]


    await update.message.reply_text(
        f"👥 Total Users: {count}"
    )



async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return


    if not context.args:

        await update.message.reply_text(
            "Use:\n/broadcast message"
        )

        return


    message = " ".join(context.args)


    cursor.execute(
        "SELECT id FROM users"
    )

    users = cursor.fetchall()


    sent = 0


    for user in users:

        try:

            await context.bot.send_message(
                chat_id=user[0],
                text=message
            )

            sent += 1

        except:
            pass



    await update.message.reply_text(
        f"✅ Broadcast sent to {sent} users"
    )



# ================= ERROR HANDLER =================


async def error_handler(update, context):

    logging.error(
        f"Error: {context.error}"
    )



# ================= BOT START =================


def main():

    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            buttons
        )
    )


    app.add_handler(
        CommandHandler(
            "reply",
            admin_reply
        )
    )


    app.add_handler(
        CommandHandler(
            "users",
            users_count
        )
    )


    app.add_handler(
        CommandHandler(
            "broadcast",
            broadcast
        )
    )


   app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        user_chat
    ),
    group=1
)


app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        ai_chat
    ),
    group=2
)
    )


    app.add_error_handler(
        error_handler
    )


    print("✅ VIRENDRA BOT STARTED")


    app.run_polling()



if __name__ == "__main__":
    main()

