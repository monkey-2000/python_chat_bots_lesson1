import logging

LOG_LEVEL = 'INFO'
_log_format = f"%(asctime)s - [%(levelname)s] - %(message)s"


class TelegramHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_file_handler(log_level=LOG_LEVEL):
    file_handler = logging.FileHandler("x.log", encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_telegrm_handler(bot, chat_id, log_level=LOG_LEVEL):
    telegrm_handler = TelegramHandler(bot, chat_id)
    telegrm_handler.setLevel(log_level)
    telegrm_handler.setFormatter(logging.Formatter(_log_format))
    return telegrm_handler


def get_stream_handler(log_level=LOG_LEVEL):
    get_stream_handler = logging.StreamHandler()
    get_stream_handler.setLevel(log_level)
    get_stream_handler.setFormatter(logging.Formatter(_log_format))
    return get_stream_handler


def get_logger(name, bot='', chat_id=''):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    if bot and chat_id:
        logger.addHandler(get_telegrm_handler(bot, chat_id))
    return logger
