from pyrogram import Client, filters
from pyrogram.types import Message

from textgen import app, logger, model, GROUP_FILTER
from textgen.bot import counter, commands

logger.info("LOGGED")


@app.on_message(
    filters.chat(GROUP_FILTER)
    & filters.text
    & filters.create(lambda *args: counter.check_threshold())
    & ~filters.command(commands),
    group=1,
)
async def threshold_message(client: Client, message: Message):
    logger.info(f"Sent message to {message.from_user.id}")
    counter.reset_count()
    await client.send_message(message.chat.id, model.generate_text())
    message.continue_propagation()
