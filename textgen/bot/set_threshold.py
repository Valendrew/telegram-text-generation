from textgen import logger

from pyrogram import Client, filters
from pyrogram.types import Message

from textgen import app, GROUP_FILTER
from textgen.bot import thresholds, counter

logger.info("LOGGED")


@app.on_message(filters.chat(GROUP_FILTER) & filters.command("threshold"), group=-2)
async def set_threshold(client: Client, message: Message):
    command_arg = message.text.split(" ", maxsplit=1)

    if len(command_arg) > 1 and command_arg[1] in thresholds.keys():
        command_arg = command_arg[1]
        logger.info(f"Set threshold for {message.chat.id} to {command_arg}")
        counter.change_threshold(thresholds[command_arg])
        await client.send_message(message.chat.id, "Set threshold")

    message.continue_propagation()
