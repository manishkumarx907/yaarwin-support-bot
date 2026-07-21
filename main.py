from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = "8907587670:AAEWj0GM9ngYuNmliBel3qCXIlPo01TBt1o"

REGISTER_LINK = "https://www.yaarwin.online/#/register?invitationCode=182763900728"
SUPPORT_USERNAME = "https://t.me/Vpnusern"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Register Now", url=REGISTER_LINK)],
        [InlineKeyboardButton("✅ I Have Registered", callback_data="menu")]
    ]

    text = (
        "👋 *Welcome to YAAR WIN SUPPORT*\n\n"
        "🎉 *Sabse pehle YAARWIN me apna account register karein.*\n\n"
        "👇 Registration karne ke liye niche button dabaye."
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        keyboard = [
            [InlineKeyboardButton("💰 Deposit", callback_data="deposit")],
            [InlineKeyboardButton("💸 Withdrawal", callback_data="withdraw")],
            [InlineKeyboardButton("🎁 Bonus", callback_data="bonus")],
            [InlineKeyboardButton("💼 Daily Salary", callback_data="salary")],
            [InlineKeyboardButton("👥 Referral", callback_data="referral")],
            [InlineKeyboardButton("📞 Customer Support", url=SUPPORT_USERNAME)],
        ]

        await query.edit_message_text(
            "✅ Registration Complete!\n\nChoose an option below:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "deposit":
        await query.answer("Deposit support available.", show_alert=True)

    elif query.data == "withdraw":
        await query.answer("Withdrawal support available.", show_alert=True)

    elif query.data == "bonus":
        await query.answer("Bonus information available.", show_alert=True)

    elif query.data == "salary":
        await query.answer("Daily Salary information available.", show_alert=True)

    elif query.data == "referral":
        await query.answer("Referral Program available.", show_alert=True)


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot Started...")
app.run_polling()
