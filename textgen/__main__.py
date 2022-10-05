from email.mime import message
import os

from pyrogram import Client, filters
from pyrogram.types import Message

from .Counter import Counter
from . import ngram
from textgen import (
    API_HASH,
    API_ID,
    BOT_NAME,
    BOT_TOKEN,
    TELEGRAM_IDS,
    GROUP_FILTER,
    logger,
)

model = ngram.NGramModel(n=3, tokenizer=True)
app = Client(
    BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir=os.path.join(os.path.dirname(__file__), "data"),
)
commands = ["generate", "threshold"]
thresholds = {"low": 30, "normal": 20, "high": 10}

counter = Counter(thresholds["normal"])


@app.on_message(
    filters.chat(GROUP_FILTER) & filters.text & ~filters.command(commands), group=0
)
async def count_message(client: Client, message: Message):
    counter.increase_count()
    message.continue_propagation()


@app.on_message(
    filters.chat(GROUP_FILTER)
    & filters.text
    & filters.create(lambda *args: counter.check_threshold())
    & ~filters.command(commands),
    group=1,
)
async def send_threshold_message(client: Client, message: Message):
    logger.info(f"Sent message to {message.from_user.id}")
    counter.reset_count()
    await client.send_message(message.chat.id, model.generate_text())
    message.continue_propagation()


@app.on_message(filters.chat(GROUP_FILTER) & filters.command("generate"), group=-1)
async def send_generated_message(client: Client, message: Message):
    logger.info(f"Sent message to {message.chat.id}")
    text = model.generate_text()
    await client.send_message(message.chat.id, text)
    message.continue_propagation()


@app.on_message(filters.chat(GROUP_FILTER) & filters.command("threshold"), group=-2)
async def set_threshold(client: Client, message: Message):
    command_arg = message.text.split(" ", maxsplit=1)

    if len(command_arg) > 1 and command_arg[1] in thresholds.keys():
        command_arg = command_arg[1]
        logger.info(f"Set threshold for {message.chat.id} to {command_arg}")
        counter.change_threshold(thresholds[command_arg])
        await client.send_message(message.chat.id, "Set threshold")

    message.continue_propagation()


if __name__ == "__main__":
    PARSER = "telegram"
    DATA_FILE = "result.json"

    if PARSER == "telegram":
        raw_data = ngram.TelegramParser.parse_file(DATA_FILE, TELEGRAM_IDS)

    # small_raw_data = raw_data[0:50]
    model.train(raw_data)

    app.run()
