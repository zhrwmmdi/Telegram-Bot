from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler, InlineQueryHandler, \
    ConversationHandler
from os import remove

from local_utils import TOKEN

CAPTION, IMAGE = range(2)
database = {}


async def start_conversation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='You started a new conversation. Now, send a caption.'
    )
    return CAPTION


async def caption_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database[update.effective_chat.id] = update.message.text
    await context.bot.send_message(
        text="ok now send me your image",
        chat_id=update.effective_chat.id,
    )
    return IMAGE


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image = await update.message.photo[-1].get_file()
    download = await image.download_to_drive('user.png')
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=download,
        caption=database[update.effective_chat.id],
    )
    remove(download)
    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="you just canceled the conversation"
    )
    return ConversationHandler.END

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('conversation', start_conversation_handler),],
        states={
            CAPTION: [MessageHandler(filters.TEXT, caption_handler),],
            IMAGE: [MessageHandler(filters.PHOTO, photo_handler),],
        },
        fallbacks=[MessageHandler(filters.ALL, cancel_handler),],
        allow_reentry=True,
    )

    application.add_handler(conversation_handler)
    application.run_polling()
