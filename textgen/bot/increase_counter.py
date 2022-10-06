from pyrogram import Client, filters
from pyrogram.types import Message

from textgen import app, logger, GROUP_FILTER
from textgen.bot import commands, counter

logger.info("LOGGED")


@app.on_message(
    filters.chat(GROUP_FILTER) & filters.text & ~filters.command(commands), group=0
)
async def increase_counter(client: Client, message: Message):
    counter.increase_count()
    message.continue_propagation()
