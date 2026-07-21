
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8907587670:AAEWj0GM9ngYuNmliBel3qCXIlPo01TBt1o"

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

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("contact", contact))
print("Bot Started...")
app.run_polling()
