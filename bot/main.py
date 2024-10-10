import telebot
import telebot.types as types
from environs import Env

import messages
from handlers import DBTokensHandler
from tools import logger, logger_obj

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

bot = telebot.TeleBot(token=BOT_TOKEN)


@bot.message_handler(commands=["start"])
@logger
def start(message: types.Message) -> None:
    """Send welcome message to User, set new User token.

    Args:
        message: /start command form User.

    """
    bot.send_message(message.from_user.id, messages.WELCOME_MSG)
    set_new_token(message)


@bot.message_handler(commands=["new_token"])
@logger
def set_new_token(message: types.Message) -> None:
    """Set new token for User.

    Args:
        message: /new_token command from User.

    """
    user_token = DBTokensHandler.update_me(message) if DBTokensHandler.get_me(message)\
        else DBTokensHandler.set_me(message)
    bot.send_message(message.from_user.id, messages.MY_NEW_TOKEN_SET_MSG(user_token))


@bot.message_handler(commands=["my_token"])
@logger
def my_token(message: types.Message) -> None:
    """Tell User their token.

    Args:
        message: /my_token command from User.

    """
    user_token = DBTokensHandler.get_me(message)
    msg = messages.MY_TOKEN_MSG(user_token) if user_token else messages.MY_TOKEN_NOT_FOUND_MSG
    bot.send_message(message.from_user.id, msg)


@bot.message_handler(commands=["set_recipient"])
@logger
def set_recipient(message: types.Message) -> None:
    """Send new Recipient's token request to User.

    Args:
        message: /set_recipient command from User.

    """
    bot.send_message(message.from_user.id,
                     messages.SET_RECIPIENT_MSG,
                     reply_markup=types.ForceReply(input_field_placeholder=messages.SET_RECIPIENT_PLACEHOLDER))


@bot.message_handler(func=lambda message: message.reply_to_message\
                                          and message.reply_to_message.text == messages.SET_RECIPIENT_MSG)
@logger
def new_recipient(message: types.Message) -> None:
    """Set new Recipient's token from User's input.

    Args:
        message: Text message with new Recipient's token.

    """
    recipient_token = DBTokensHandler.set_recipient(message)
    bot.send_message(message.from_user.id, messages.NEW_RECIPIENT_MSG(recipient_token))


@bot.message_handler(commands=["delete_recipient"])
@logger
def delete_recipient(message: types.Message) -> None:
    """Set current Recipient's token to null.

    Args:
        message: /delete_recipient command from User.

    """
    DBTokensHandler.delete_recipient(message)
    bot.send_message(message.from_user.id, messages.RECIPIENT_DELETE_MSG)


@bot.message_handler(commands=["get_recipient"])
@logger
def get_recipient(message: types.Message) -> None:
    """Tell User current Recipient's token.

    Args:
        message: /get_recipient command from User.

    """
    current_recipient = DBTokensHandler.get_recipient(message)
    bot.send_message(message.from_user.id, messages.GET_RECIPIENT_MSG(current_recipient))


@bot.message_handler(commands=["random_recipient"])
@logger
def random_recipient(message: types.Message) -> None:
    """Set a random Recipient from existing in the DB.

    Args:
        message: /random_recipient command from User.

    """
    recipient_token = DBTokensHandler.set_random_recipient(message)
    bot.send_message(message.from_user.id, messages.NEW_RECIPIENT_MSG(recipient_token))


@bot.message_handler(func=lambda message: not message.reply_to_message)
@logger
def send_message(message: types.Message) -> None:
    """Send anonymous text message to chosen Recipient. Tell User weather the message has been sent or not.

    Args:
        message: Text message from User.

    """
    recipient_token = DBTokensHandler.get_recipient(message)
    sender_token = DBTokensHandler.get_me(message)
    if recipient_id := DBTokensHandler.get_recipient_id(message):
        bot.send_message(recipient_id, messages.INCOMING_MESSAGE_MSG(sender_token, message.text))
        bot.send_message(message.from_user.id, messages.MESSAGE_SENT_MSG(recipient_token))
    else:
        bot.send_message(message.from_user.id, messages.RECIPIENT_NOT_FOUND_MSG(recipient_token))


def main():
    logger_obj.info("Bot is running.")
    bot.infinity_polling()


if __name__ == '__main__':
    main()
