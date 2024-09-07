from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler, InlineQueryHandler, \
    ConversationHandler
from os import remove

from local_utils import TOKEN

GENDER, PHOTO, BIO = range(3)


async def start_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("Hi, I'm here to find out more information about you."
                "You can /cancel me at any time you want.\n\n"
                "Are you a Boy or a Girl?"),
        reply_to_message_id=update.effective_message.id,
    )
    return GENDER


async def gender_message_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("Okay, Now can you please send me a photo of your self."
                "If you don't want to do that, you can /skip this state."),
        reply_to_message_id=update.effective_message.id,
    )
    return PHOTO


async def photo_message_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    image = await update.effective_message.photo[-1].get_file()
    download = await image.download_to_drive(f'photos/user_{update.effective_user.id}.jpg')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Okay, Now can you please send me a bio about yourself.',
        reply_to_message_id=update.effective_message.id,
    )
    return BIO


async def skip_photo_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Okay, Now can you please send me a bio about yourself.',
        reply_to_message_id=update.effective_message.id,
    )
    return BIO


async def bio_message_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Thank you! I hope we can talk again some day.',
        reply_to_message_id=update.effective_message.id,
    )
    return ConversationHandler.END


async def cancel_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Bye! I hope we can talk again some day.',
        reply_to_message_id=update.effective_message.id,
    )
    return ConversationHandler.END

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command_handler)],
        states={
            GENDER: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, gender_message_handler
                )
            ],
            PHOTO: [
                MessageHandler(filters.PHOTO, photo_message_handler),
                CommandHandler("skip", skip_photo_command_handler),
            ],
            BIO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, bio_message_handler)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command_handler),
        ],
        allow_reentry=True,
    )

    app.add_handler(conversation_handler)
    app.run_polling()
