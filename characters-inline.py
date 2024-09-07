from uuid import uuid4

import requests
from telegram import InlineQueryResultPhoto, Update
from telegram.ext import Application, InlineQueryHandler, ContextTypes

from local_utils import TOKEN



async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    data = requests.get("https://thronesapi.com/api/v2/Characters")
    data = data.json()

    characters = {}
    for d in data:
        characters[d["fullName"]] = d["imageUrl"]

    results = []
    if not query:
        for name, url in characters.items():
            new_item = InlineQueryResultPhoto(
                id=str(uuid4()),
                photo_url=url,
                thumbnail_url=url,
                caption=name
            )
            results.append(new_item)
    else:
        for name, url in characters.items():
            if query in name:
                new_item = InlineQueryResultPhoto(
                    id=str(uuid4()),
                    photo_url=url,
                    thumbnail_url=url,
                    caption=name
                )
                results.append(new_item)
    await update.inline_query.answer(results, auto_pagination=True)


if __name__=="__main__":
    # Create the Application and pass it your bot's token
    application=Application.builder().token(TOKEN).build()

    application.add_handler(InlineQueryHandler(inline_query_handler))
    # Run the Bot
    application.run_polling()