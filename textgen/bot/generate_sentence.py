from pyrogram import Client, filters
from pyrogram.types import Message

from textgen import app, logger, model, GROUP_FILTER

logger.info("LOGGED")


@app.on_message(filters.chat(GROUP_FILTER) & filters.command("generate"), group=-1)
async def send_generated_message(client: Client, message: Message):
    logger.info(f"Sent message to {message.chat.id}")
    text = model.generate_text()
    await client.send_message(message.chat.id, text)
    message.continue_propagation()
