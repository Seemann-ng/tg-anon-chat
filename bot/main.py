import logging

import telebot
import telebot.types as types

import credentials
from dbtokenshandler import DBTokensHandler as TokenHandler

bot = telebot.TeleBot(token=credentials.BOT_TOKEN)

logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    """Send welcome message to User, set new User token.

    Args:
        message: /start command form User.

    """
    logging.info("start() enter.")
    bot.send_message(message.from_user.id, "Hello! Welcome to my chatbot!")
    set_new_token(message)
    logging.info("start() done.")


@bot.message_handler(commands=["new_token"])
def set_new_token(message: types.Message) -> None:
    """Set new token for User.

    Args:
        message: /new_token command from User.

    """
    logging.info("set_new_token() enter.")
    if not TokenHandler.get_my_token(message):
        user_token = TokenHandler.set_my_token(message)
    else:
        user_token = TokenHandler.update_my_token(message)
    bot.send_message(message.from_user.id, f"Your new user token: {user_token}")
    logging.info("set_new_token() done.")


@bot.message_handler(commands=["my_token"])
def my_token(message: types.Message) -> None:
    """Tell User their token.

    Args:
        message: /my_token command from User.

    """
    logging.info("my_token() enter.")
    user_token = TokenHandler.get_my_token(message)
    if user_token:
        bot.send_message(message.from_user.id, f"Your token: {user_token}")
        logging.info("my_token() done (200).")
    else:
        bot.send_message(message.from_user.id, "Token was not found.")
        logging.info("my_token() done (404).")


@bot.message_handler(commands=["set_recipient"])
def set_recipient(message: types.Message) -> None:
    """Send new Recipient's token request to User.

    Args:
        message: /set_recipient command from User.

    """
    logging.info("set_recipient() enter.")
    bot.send_message(
        message.from_user.id,
        "Please enter new Recipient's token.",
        reply_markup=types.ForceReply(input_field_placeholder="Recipient's token")
    )
    logging.info("set_recipient() done.")


@bot.message_handler(
    func=lambda m: m.reply_to_message and m.reply_to_message.text == "Please enter new recipient token."
)
def new_recipient(message: types.Message) -> None:
    """Set new Recipient's token from User's input.

    Args:
        message: Text message with new Recipient's token.

    """
    logging.info("new_recipient() enter.")
    recipient_token = TokenHandler.set_recipient_token(message)
    bot.send_message(message.from_user.id, f"Your recipient is now: {recipient_token}.")
    logging.info("new_recipient() done.")


@bot.message_handler(commands=["delete_recipient"])
def delete_recipient(message: types.Message) -> None:
    """Set current Recipient's token to null.

    Args:
        message: /delete_recipient command from User.

    """
    logging.info("delete_recipient() enter.")
    TokenHandler.delete_recipient_token(message)
    bot.send_message(message.from_user.id, "Your recipient was set to null.")
    logging.info("delete_recipient() done.")


@bot.message_handler(commands=["get_recipient"])
def get_recipient(message: types.Message) -> None:
    """Tell User current Recipient's token.

    Args:
        message: /get_recipient command from User.

    """
    logging.info("get_recipient() enter.")
    current_recipient = TokenHandler.get_recipient_token(message)
    bot.send_message(message.from_user.id, f"Your recipient is: {current_recipient}.")
    logging.info("get_recipient() done.")


@bot.message_handler(commands=["random_recipient"])
def random_recipient(message: types.Message) -> None:
    """Set a random Recipient from existing in the DB.

    Args:
        message: /random_recipient command from User.

    """
    logging.info("random_recipient() enter.")
    recipient_token = TokenHandler.set_random_recipient_token(message)
    bot.send_message(message.from_user.id, f"Your recipient is now: {recipient_token}.")
    logging.info("random_recipient() done.")


@bot.message_handler(func=lambda message: True)
def send_message(message: types.Message) -> None:
    """Send anonymous text message to chosen Recipient. Tell User weather the message has been sent or not.

    Args:
        message: Text message from User.

    """
    logging.info("send_message() enter.")
    recipient_id = TokenHandler.get_recipient_id(message)
    recipient_token = TokenHandler.get_recipient_token(message)
    sender_token = TokenHandler.get_my_token(message)
    if recipient_id:
        bot.send_message(recipient_id, f"Incoming message from {sender_token}:\n{message.text}")
        bot.send_message(message.from_user.id, f"Your message has been sent to {recipient_token}.")
        logging.info("send_message() done (sent).")
    else:
        bot.send_message(
            message.from_user.id,
            f"Recipient {recipient_token} was not found.\nYour message has NOT been sent."
        )
        logging.info("send_message() done (NOT sent).")


def main():
    logging.info("Bot is running.")
    bot.infinity_polling()


if __name__ == '__main__':
    main()
