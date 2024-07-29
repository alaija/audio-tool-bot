from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from logger import logger
import os
import transcriber
import llm

CLEAN_UP, STRUCTURE, TRANSLATE_DE, TRANSLATE_EN, EMAIL_DE, EMAIL_EN = range(6)

def inline_keyboard_markup():
    keyboard = [ 
        [
            InlineKeyboardButton("🧽", callback_data=CLEAN_UP),
            InlineKeyboardButton("🏗️", callback_data=STRUCTURE),
        ],
        [
            InlineKeyboardButton("🇬🇧", callback_data=TRANSLATE_EN),
            InlineKeyboardButton("🇩🇪", callback_data=TRANSLATE_DE),
        ],
        [
            InlineKeyboardButton("📧 🇬🇧", callback_data=EMAIL_EN),
            InlineKeyboardButton("📧 🇩🇪", callback_data=EMAIL_DE),
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(f"Hi {user.full_name}!")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle audio messages."""        
    messages = []
    messages.append(await update.message.reply_text("🦻"))

    message = update.message

    file = await message.effective_attachment.get_file()
    file_path = message.effective_attachment.file_id
    
    if not os.path.exists(file_path):
        logger.info(f"Downloading file '{file_path}'")
        await file.download_to_drive(file_path)

    response = transcriber.transcribe(file_path)
    
    if os.path.exists(file_path):
        os.remove(file_path)

    for message in messages:
        await message.delete()

    await update.message.reply_text(f'{response.strip()}', reply_markup=inline_keyboard_markup())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer(cache_time=60)

    await query.edit_message_text(text="📝", reply_markup=None)
    
    if query.data == str(CLEAN_UP):
        response = llm.clean_up(query.message.text)
    elif query.data == str(STRUCTURE):
        response = llm.structure(query.message.text)
    elif query.data == str(TRANSLATE_DE):
        response = llm.translate("German", query.message.text)
    elif query.data == str(TRANSLATE_EN):
        response = llm.translate("English", query.message.text)
    elif query.data == str(EMAIL_DE):
        response = llm.email("German", query.message.text)
    elif query.data == str(EMAIL_EN):
        response = llm.email("English", query.message.text)

    await query.edit_message_text(text=response, reply_markup=inline_keyboard_markup(), parse_mode="Markdown")
    
def start(token: str) -> None:
    """Start the bot."""
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE, handle_audio))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)