from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TOKEN")

AFFILIATE_LINK = "https://stake.bet/?c=LeBonPronoVIP"
VIP_LINK = "https://t.me/+nWe-miC_XLJkZmY0"

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔥 Accéder", callback_data="go")]]

    await update.message.reply_text(
        "👋 Bienvenue !",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "go":
        user_state[q.from_user.id] = "link"

        await q.edit_message_text(
            "👉 Clique ici puis reviens 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Ouvrir", url=AFFILIATE_LINK)],
                [InlineKeyboardButton("✅ C’est fait", callback_data="done")]
            ])
        )

    elif q.data == "done":
        user_state[q.from_user.id] = "pseudo"
        await q.edit_message_text("✍️ Envoie ton pseudo :")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id

    if user_state.get(uid) == "pseudo":
        await update.message.reply_text(
            f"✅ Merci !\n\nVIP ici 👇\n{VIP_LINK}"
        )
        user_state[uid] = "done"

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
