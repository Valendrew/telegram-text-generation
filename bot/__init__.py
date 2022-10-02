import configparser
import logging

config = configparser.ConfigParser()
config.read("config.ini")

TELEGRAM_IDS = [int(v) for v in config.get('TELEGRAM_CHAT', 'ids', fallback='').split()]

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)