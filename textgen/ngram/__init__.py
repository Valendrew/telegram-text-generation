import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

from .classes.NGramModel import NGramModel
from .classes.TelegramParser import TelegramParser