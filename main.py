
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
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


REGISTER_LINK = "https://www.yaarwin.online/#/register?invitationCode=182763900728"
SUPPORT_USERNAME = "https://t.me/Vpnusern"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🟢 Register Now", url=REGISTER_LINK)],
        [InlineKeyboardButton("✅ I Have Registered", callback_data="menu")]
    ]

    await update.message.reply_text(
        "👋 Welcome to YAARWIN SUPPORT BOT\n\nPlease register first.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "menu":

        keyboard = [
            [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
            [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")],
            [InlineKeyboardButton("🎁 Bonus", callback_data="bonus")],
            [InlineKeyboardButton("💼 Daily Salary", callback_data="salary")],
            [InlineKeyboardButton("👥 Referral", callback_data="referral")],
            [InlineKeyboardButton("📞 Customer Support", url=SUPPORT_USERNAME)]
        ]

        await query.edit_message_text(
            "✅ Registration Completed!\n\nChoose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "deposit":
        await query.message.reply_text(
            "💰 Deposit Support\nPlease contact customer support."
        )

    elif query.data == "withdraw":
        await query.message.reply_text(
            "💸 Withdrawal Support\nPlease contact customer support."
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
            "👥 Referral information will be updated soon."
        )


# AI CHAT
async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        user_text = update.message.text

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are YAARWIN support agent. Reply like a real human. Use Hindi and English both."
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
        await update.message.reply_text(
            "Sorry, please try again later."
        )


app = Application.builder().token(BOT_TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

# AI messages
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat)
)


print("YAARWIN BOT STARTED")

app.run_polling()
