import functools
import logging

import telebot.types as types

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger_obj = logging.getLogger("Telegraph Chat")


def logger(func):
    @functools.wraps(func)
    def wrapper(message: types.Message, *args, **kwargs):
        logger_obj.info(f"{func.__name__} called by user {message.from_user.username} with message {message.text}.")
        result = func(message, *args, **kwargs)
        logger_obj.info(f"{func.__name__} executed successfully.")
        return result

    return wrapper
