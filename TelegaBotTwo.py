from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def Hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Эй, {update.message.from_user.first_name}!, тебе че надо?')


app = ApplicationBuilder().token("6581992513:AAFSuk41_gC3avbA70xqcCpJUx1xXChBzMo").build()
app.add_handler(CommandHandler("hello", Hello))
app.run_polling()
