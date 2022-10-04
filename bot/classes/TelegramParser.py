import json
import time
from bot import TELEGRAM_IDS, logger
import pickle


class TelegramParser:
    BINARY_FILE = "telegram.pickle"

    @staticmethod
    def read_file(filename: str, specific_ids: list[int] = []) -> list:
        """Reads the json file as a dictionary

        Args:
            filename (str): file to read
            specific_ids (list[int], optional): specific chat ids to filter. Defaults to [].

        Returns:
            list: list of raw messages
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            chats: list = data["chats"]["list"]
            if len(specific_ids) > 0:
                return [v["messages"] for v in chats if v["id"] in specific_ids]
            else:
                return chats
        except Exception as err:
            logger.error(err)

    @staticmethod
    def filter_file(data: list, message_type: list[str] = ["message"]) -> list:
        """Filter raw file by selecting only specific types

        Args:
            data (list): raw data read
            message_type (list[str], optional): types of messages to filter. Defaults to ["message"].

        Returns:
            list: list of filter messages
        """
        raw_data = [
            msg["text"]
            for chat in data
            for msg in chat
            if (
                msg["type"] in message_type
                and isinstance(msg["text"], str)
                and len(msg["text"]) > 0
            )
        ]
        with open(TelegramParser.BINARY_FILE, "wb") as f:
            pickle.dump(raw_data, f)

        return raw_data

    def parse_file(filename: str, force_read=False) -> list:
        start_time = time.time()

        if not force_read:
            try:
                with open(TelegramParser.BINARY_FILE, "rb") as f:
                    logger.debug("Found binary file")
                    return pickle.load(f)
            except FileNotFoundError:
                logger.debug("Binary file not found, reading JSON...")
        # Read file
        logger.debug(f"Reading telegram file: {filename}")
        raw_data = TelegramParser.read_file(filename, specific_ids=TELEGRAM_IDS)
        logger.debug(f"Found {len(raw_data)} chats")
        # Filter only messages
        raw_data = TelegramParser.filter_file(raw_data)
        logger.debug(f"Found {len(raw_data)} raw messages")
        # log file
        logger.debug(f"Time for processing: {time.time() - start_time : .2f} seconds")

        return raw_data
