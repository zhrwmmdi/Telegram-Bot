from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, ContextTypes, InlineQueryHandler
from local_utils import TOKEN


async def inlineHandle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # check if an inline request exists
    inline_request = update.inline_query
    if not inline_request:
        return

    # check if the inline query is not empty
    query = inline_request.query
    if not query:
        return

    responses = [
        InlineQueryResultArticle(id='1', title="UpperCase", input_message_content=InputTextMessageContent(query.upper())),
        InlineQueryResultArticle(id='2', title="LowerCase", input_message_content=InputTextMessageContent(query.lower())),
    ]

    await inline_request.answer(responses)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(InlineQueryHandler(inlineHandle))
    application.run_polling()
