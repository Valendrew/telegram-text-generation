from bot.classes import NGramModel, TelegramParser, NGramModelTrie
from bot import logger

if __name__ == "__main__":
    PARSER = "telegram"
    DATA_FILE = "result.json"

    if PARSER == "telegram":
        raw_data = TelegramParser.parse_file(DATA_FILE)

    # small_raw_data = raw_data[0:50]
    model = NGramModelTrie(n=3, tokenizer=True)
    model.train(raw_data)

    while True:
        input("\n--Enter to generate--")
        try:
            print(model.generate_text(10))
        except Exception as e:
            logger.error(f"ERROR: {e}")
            continue
