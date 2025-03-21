import logging
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a reaction bot.")

async def reaction(update: Update, context: CallbackContext):
    emoji = "😱"
    # Gère à la fois les messages normaux et les posts de canal
    chat_id = update.channel_post.chat_id if update.channel_post else update.message.chat_id
    message_id = update.channel_post.message_id if update.channel_post else update.message.message_id
    
    try:
        await context.bot.set_message_reaction(chat_id, message_id, reaction=[ReactionTypeEmoji(emoji)])
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout de la réaction: {e}")

print("Bot Is Working")
app = ApplicationBuilder().token("7652627861:AAHhq0HUA-15Ig71m-HY7gMp2zhzRkr4wxg").build()

start_handler = CommandHandler('start', start)
app.add_handler(start_handler)

# Handler pour les messages textuels dans les groupes, messages privés ET canaux
react_handler = MessageHandler(
    (filters.TEXT | filters.ChatType.CHANNEL) & ~filters.COMMAND, 
    reaction
)
app.add_handler(react_handler)

app.run_polling()