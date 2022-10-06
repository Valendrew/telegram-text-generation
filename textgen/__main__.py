from . import ngram
from textgen import bot
from textgen import model, app, TELEGRAM_IDS


if __name__ == "__main__":
    PARSER = "telegram"
    DATA_FILE = "result.json"

    if PARSER == "telegram":
        raw_data = ngram.TelegramParser.parse_file(DATA_FILE, TELEGRAM_IDS)

    # small_raw_data = raw_data[0:50]
    model.train(raw_data)

    app.run()
