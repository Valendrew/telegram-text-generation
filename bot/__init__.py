import configparser

config = configparser.ConfigParser()
config.read("config.ini")

TELEGRAM_IDS = [int(v) for v in config.get('TELEGRAM_CHAT', 'ids', fallback='').split()]
