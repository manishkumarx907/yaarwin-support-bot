from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

REGISTER_LINK = "https://www.yaarwin.online/#/register?invitationCode=182763900728"
SUPPORT_USERNAME = "https://t.me/Vpnusern"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Register Now", url=REGISTER_LINK)],
        [InlineKeyboardButton("✅ I Have Registered", callback_data="menu")],
    ]

    text = (
        "👋 *Welcome to YAARWIN SUPPORT BOT*\n\n"
        "🎉 Welcome!\n"
        "Please register first using the button below."
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
            [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")],
            [InlineKeyboardButton("🎁 Bonus", callback_data="bonus")],
            [InlineKeyboardButton("💼 Daily Salary", callback_data="salary")],
            [InlineKeyboardButton("👥 Referral", callback_data="referral")],
            [InlineKeyboardButton("📞 Customer Support", url=SUPPORT_USERNAME)],
        ]

        await query.edit_message_text(
            "✅ *Registration Completed!*\n\nChoose an option:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "deposit":
        await query.answer()
        await query.message.reply_text(
            "💰 Deposit Support\n\nPlease contact customer support."
        )

    elif query.data == "withdraw":
        await query.answer()
        await query.message.reply_text(
            "💸 Withdrawal Support\n\nPlease contact customer support."
        )

    elif query.data == "bonus":
        await query.answer()
        await query.message.reply_text(
            "🎁 Bonus information will be updated soon."
        )

    elif query.data == "salary":
        await query.answer()
        await query.message.reply_text(
            "💼 Daily Salary information will be updated soon."
        )

    elif query.data == "referral":
        await query.answer()
        await query.message.reply_text(
            "👥 Referral Program information will be updated soon."
        )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("✅ YAARWIN SUPPORT BOT Started...")
app.run_polling()
