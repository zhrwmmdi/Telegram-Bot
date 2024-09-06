import logging
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, \
    MessageHandler, filters
from local_utils import TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


HELP_COMMAND_RESPONSE = """
Greetings! Here are the commands you can use with this bot:

/start -> Begin interacting with the bot
/repeat <text> -> Have the bot repeat the provided text
/time -> Receive the current time from the bot
/help -> Display this message again
Feel free to utilize any of these commands as needed. If you require further assistance, don't hesitate to ask. Farewell for now!
"""

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hello dear {update.effective_user.first_name}'
    )


async def repeat_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=' '.join(context.args),
        reply_to_message_id=update.effective_message.id
    )


async def time_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        reply_to_message_id=update.effective_message.id
    )


async def help_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_COMMAND_RESPONSE,
        reply_to_message_id=update.effective_message.id
    )


async def upper_case_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text.upper(),
        reply_to_message_id=update.effective_message.id
    )


async def echo_sticker_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_sticker(
        chat_id=update.effective_chat.id,
        sticker=update.effective_message.sticker,
        reply_to_message_id=update.effective_message.id
    )

if __name__=="__main__":
    # Create the Application and pass it your bot's token
    application=Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start_handler))
    # application.add_handler(MessageHandler(filters.TEXT, echo_handler))
    application.add_handler(MessageHandler(filters.TEXT, upper_case_message_handler))
    application.add_handler(MessageHandler(filters.Sticker.ALL, echo_sticker_message_handler))
    application.add_handler(CommandHandler('repeat', repeat_command_handler))
    application.add_handler(CommandHandler('help', help_command_handler))
    application.add_handler(CommandHandler('time', time_command_handler))
    # Run the Bot
    application.run_polling()

