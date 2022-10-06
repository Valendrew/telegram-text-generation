# Configuration
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

TELEGRAM_IDS = [int(v) for v in config.get("TELEGRAM_CHAT", "ids", fallback="").split()]
BOT_NAME = config.get("BOT", "name", fallback="")
BOT_TOKEN = config.get("BOT", "token", fallback="")
API_ID = config.getint("BOT", "id", fallback=0)
API_HASH = config.get("BOT", "hash", fallback="")
GROUP_FILTER = config.getint("BOT", "group", fallback=0)

# Logging
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# NGram model
from . import ngram

model = ngram.NGramModel(n=3, tokenizer=True)

# Telegram Client
import os
from pyrogram import Client

app = Client(
    BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir=os.path.join(os.path.dirname(__file__), "data"),
)
