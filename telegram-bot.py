import logging
import os
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "7652627861:AAHhq0HUA-15Ig71m-HY7gMp2zhzRkr4wxg"
WEBHOOK_URL = "https://ton-app-render.onrender.com/webhook"  # Remplace par l'URL de ton app Render

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a reaction bot.")

async def reaction(update: Update, context: CallbackContext):
    emoji = "😱"
    chat_id = update.channel_post.chat_id if update.channel_post else update.message.chat_id
    message_id = update.channel_post.message_id if update.channel_post else update.message.message_id
    
    try:
        await context.bot.set_message_reaction(chat_id, message_id, reaction=[ReactionTypeEmoji(emoji)])
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout de la réaction: {e}")

print("Bot Is Working")
app = ApplicationBuilder().token(TOKEN).build()

start_handler = CommandHandler('start', start)
app.add_handler(start_handler)

react_handler = MessageHandler(
    (filters.TEXT | filters.ChatType.CHANNEL) & ~filters.COMMAND, 
    reaction
)
app.add_handler(react_handler)

# Configuration du Webhook au lieu du Polling
PORT = int(os.environ.get("PORT", 8443))
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path="webhook",
    webhook_url=WEBHOOK_URL
)
