import configparser
import logging

config = configparser.ConfigParser()
config.read("config.ini")

TELEGRAM_IDS = [int(v) for v in config.get("TELEGRAM_CHAT", "ids", fallback="").split()]

BOT_NAME = config.get("BOT", "name", fallback="")
BOT_TOKEN = config.get("BOT", "token", fallback="")
API_ID = config.getint("BOT", "id", fallback=0)
API_HASH = config.get("BOT", "hash", fallback="")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

from .ngram import TelegramParser, NGramModel
