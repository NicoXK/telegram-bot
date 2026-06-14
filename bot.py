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
        "👋 Bienvenue sur LeBonPronoVIP !\n\n"
        "Clique sur le bouton ci-dessous pour accéder à la suite 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "go":
        user_state[q.from_user.id] = "link"

        await q.edit_message_text(
            "🔥 Pour accéder au VIP, inscris-toi via mon lien partenaire.\n\n"
            "✅ Une fois inscrit, reviens ici et clique sur « C’est fait ».",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Ouvrir le lien", url=AFFILIATE_LINK)],
                [InlineKeyboardButton("✅ C’est fait", callback_data="done")]
            ])
        )

    elif q.data == "done":
        user_state[q.from_user.id] = "pseudo"
        await q.edit_message_text(
            "✍️ Envoie maintenant ton pseudo Stake pour que je puisse vérifier ton inscription."
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id

    if user_state.get(uid) == "pseudo":
        pseudo_stake = update.message.text
        user = update.message.from_user

        username = f"@{user.username}" if user.username else "Pas de pseudo Telegram"
        first_name = user.first_name or "Non renseigné"

        print("🔥 Nouvelle demande VIP")
        print(f"Pseudo Telegram : {username}")
        print(f"Prénom : {first_name}")
        print(f"ID Telegram : {uid}")
        print(f"Pseudo Stake : {pseudo_stake}")

        await update.message.reply_text(
            "✅ Merci ! Ta demande a bien été reçue.\n\n"
            "Je vais vérifier ton inscription et t’ajouter au VIP manuellement."
        )

        user_state[uid] = "done"

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
