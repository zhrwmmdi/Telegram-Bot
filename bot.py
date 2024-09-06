from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from local_utils import token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!, start command is given"
    )

if __name__ == '__main__':
    # stage1: build an application with the token
    # stage2: build the command handler you want and link it to a method
    # stage3: add the command handler to the application
    # stage4: run the application

    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()
