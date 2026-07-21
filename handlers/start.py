from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome to YAARWIN SUPPORT BOT*\n\n"
        "Choose an option below:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
