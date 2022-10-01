import random
import time
from bot import TELEGRAM_IDS
from bot.classes import TextPreProcessor
from bot.classes import NGramModel
from bot.util.telegram_parser import read_telegram_file, parse_telegram_file

if __name__ == "__main__":
    PARSER = "telegram"
    DATA_FILE = "result.json"

    if PARSER == "telegram":
        start_time = time.time()
        print(f"Reading telegram file: {DATA_FILE}")
        input_data = read_telegram_file(DATA_FILE, specific_ids=TELEGRAM_IDS)
        print(f"Found {len(input_data)} chats")
        raw_data = parse_telegram_file(input_data)
        print(f"Found {len(raw_data)} raw messages")
        print(f"Time for processing: {time.time() - start_time : .2f} seconds")

    # small_raw_data = raw_data[0:50]
    data_processor = TextPreProcessor()
    model = NGramModel(3)

    for data in data_processor.pre_process_docs(raw_data):
        model.update(data)
    print("Performed cleaning")

    print("Generating text")
    while True:
        input("")
        try:
            print(model.generate_text(10))
        except Exception as e:
            print(f"ERROR: {e}")
            continue