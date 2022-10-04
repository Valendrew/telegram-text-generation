from pyrogram import Client, filters
from pyrogram.types import Message

from bot.classes import TelegramParser, NGramModelTrie
from bot import API_HASH, API_ID, BOT_NAME, BOT_TOKEN, logger

model = NGramModelTrie(n=3, tokenizer=True)
app = Client(BOT_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command('generate'))
async def send_generated_text(client: Client, message: Message):
    logger.debug(f"Sent message to {message.from_user.id}")
    text = model.generate_text(10)
    await client.send_message(chat_id=message.chat.id, text=text)

if __name__ == "__main__":
    PARSER = "telegram"
    DATA_FILE = "result.json"

    if PARSER == "telegram":
        raw_data = TelegramParser.parse_file(DATA_FILE)

    # small_raw_data = raw_data[0:50]
    model.train(raw_data)

    # print()
    app.run()
