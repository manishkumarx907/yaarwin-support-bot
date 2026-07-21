from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import SUPPORT_LINK

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "deposit":
        await query.message.reply_text(
            "💰 Deposit Support\n\nPlease contact customer support."
        )

    elif query.data == "withdraw":
        await query.message.reply_text(
            "💸 Withdrawal Support\n\nPlease contact customer support."
        )

    elif query.data == "profile":
        user = query.from_user
        await query.message.reply_text(
            f"👤 Profile\n\n"
            f"Name: {user.first_name}\n"
            f"Username: @{user.username if user.username else 'Not Set'}\n"
            f"ID: {user.id}"
        )

    elif query.data == "support":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📞 Contact Support", url=SUPPORT_LINK)]
        ])

        await query.message.reply_text(
            "Need help? Contact our support team.",
            reply_markup=keyboard
        )
