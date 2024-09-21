import random
import logging

import psycopg2
import telebot.types as types

import credentials as credentials

logging.basicConfig(
    filename="log.txt",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

conn = psycopg2.connect(
    database=credentials.DB,
    host=credentials.DB_HOST,
    user=credentials.DB_USER,
    password=credentials.DB_PASSWORD,
    port=credentials.DB_PORT
)
cursor = conn.cursor()


class DBTokensHandler:
    @staticmethod
    def update_my_token(message: types.Message) -> str:
        """Set new token for User if one exists.

        Args:
            message: Message object.

        Returns:
            User token.

        """
        logging.info("update_my_token() enter.")
        user_id = message.from_user.id
        user_token = abs(hash(str(user_id - message.id + message.date)))
        cursor.execute(
            "UPDATE users SET username = %s, user_token = %s WHERE user_id = %s",
            (message.from_user.username, user_token, user_id)
        )
        conn.commit()
        logging.info("update_my_token() exit.")
        return str(user_token)

    @staticmethod
    def set_my_token(message: types.Message) -> str:
        """Set new token for User if none exists.

        Args:
            message: Message object.

        Returns:
            User token.

        """
        logging.info("set_my_token() enter.")
        user_id = message.from_user.id
        user_token = abs(hash(str(user_id - message.id + message.date)))
        cursor.execute(
            "INSERT INTO users (username, user_id, user_token) VALUES (%s, %s, %s)",
            (message.from_user.username, user_id, user_token)
        )
        conn.commit()
        logging.info("set_my_token() exit.")
        return str(user_token)

    @staticmethod
    def get_my_token(message: types.Message) -> str | None:
        """Get User token from the DB.

        Args:
            message: Message object.

        Returns:
            User token if exists, None otherwise.

        """
        logging.info("get_my_token() enter.")
        user_id = message.from_user.id
        cursor.execute("SELECT user_token FROM users WHERE users.user_id = %s", (user_id,))
        user_token = cursor.fetchone()
        if user_token:
            logging.info("get_my_token() exit (str).")
            return user_token[0]
        logging.info("get_my_token() exit (None).")
        return None

    @staticmethod
    def set_recipient_token(message: types.Message) -> str:
        """Set new Recipient token for User.

        Args:
            message: Message object from User with new token in it.

        Returns:
            New Recipient token.

        """
        logging.info("set_recipient_token() enter.")
        if not DBTokensHandler.get_my_token(message):
            DBTokensHandler.set_my_token(message)
        recipient_token = message.text
        for symbol in recipient_token:
            if not symbol.isdigit():
                recipient_token = recipient_token.replace(symbol, '')
        cursor.execute(
            "UPDATE users SET current_recipient = %s WHERE user_id = %s",
            (recipient_token, message.from_user.id)
        )
        conn.commit()
        logging.info("set_recipient_token() exit.")
        return str(recipient_token)

    @staticmethod
    def set_random_recipient_token(message: types.Message) -> str | None:
        """Set random Recipient token from existing tokens in the DB except User's one.

        Args:
            message: Message object.

        Returns:
            New Recipient token if set, otherwise None.

        """
        logging.info("set_random_recipient_token() enter.")
        if not DBTokensHandler.get_my_token(message):
            DBTokensHandler.set_my_token(message)
        cursor.execute(
            "SELECT user_token FROM users WHERE users.user_id != %s",
            (message.from_user.id,)
        )
        recipient_tokens = cursor.fetchall()
        if recipient_tokens:
            recipient_token = recipient_tokens[random.randint(0, len(recipient_tokens) - 1)]
            cursor.execute(
                "UPDATE users SET current_recipient = %s WHERE user_id = %s",
                (recipient_token, message.from_user.id)
            )
            conn.commit()
            logging.info("set_random_recipient_token() exit (str).")
            return str(recipient_token[0])
        logging.info("set_random_recipient_token() exit (None).")
        return None

    @staticmethod
    def get_recipient_token(message: types.Message) -> str | None:
        """Get Recipient token from the DB.

        Args:
            message: Message object.

        Returns:
            Recipient token if exists, None otherwise.

        """
        logging.info("get_recipient_token() enter.")
        if not DBTokensHandler.get_my_token(message):
            DBTokensHandler.set_my_token(message)
        user_id = message.from_user.id
        cursor.execute("SELECT current_recipient FROM users WHERE user_id = %s", (user_id,))
        current_recipient = cursor.fetchone()
        if current_recipient:
            logging.info("get_recipient_token() exit (str).")
            return current_recipient[0]
        logging.info("get_recipient_token() exit (None).")
        return None

    @staticmethod
    def delete_recipient_token(message: types.Message) -> None:
        """Delete Recipient token form the DB.

        Args:
            message: Message object.

        """
        logging.info("delete_recipient_token() enter.")
        if not DBTokensHandler.get_my_token(message):
            DBTokensHandler.set_my_token(message)
        cursor.execute(
            "UPDATE users SET current_recipient = null WHERE user_id = %s",
            (message.from_user.id,)
        )
        conn.commit()
        logging.info("delete_recipient_token() exit.")

    @staticmethod
    def get_recipient_id(message: types.Message) -> int | None:
        """Get Recipient ID form the DB.

        Args:
            message: Message object.

        Returns:
            Recipient ID if found, None otherwise.

        """
        logging.info("get_recipient_id() enter.")
        if not DBTokensHandler.get_my_token(message):
            DBTokensHandler.set_my_token(message)
        current_recipient = DBTokensHandler.get_recipient_token(message)
        if current_recipient:
            cursor.execute(
                "SELECT user_id FROM users WHERE user_token = %s",
                (current_recipient,)
            )
            recipient_id = cursor.fetchone()
            if recipient_id:
                logging.info("get_recipient_id() exit (str).")
                return recipient_id[0]
            logging.info("get_recipient_id() exit (None recipient_id).")
            return None
        logging.info("get_recipient_id() exit (None current_recipient).")
        return None
