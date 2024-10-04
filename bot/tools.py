import functools
import logging

import telebot.types as types

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("Telegraph Chat")


def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(message: types.Message, *args, **kwargs):
        logger.info(f"{func.__name__} called by user {message.from_user.username} with message {message.text}")
        return func(message, *args, **kwargs)
    return wrapper
