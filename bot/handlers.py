import random

import psycopg2
import telebot.types as types
from environs import Env

env = Env()
env.read_env()

DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")


def cur():
    conn = psycopg2.connect(database="postgres",
                            user=DB_USER,
                            password=DB_PASSWORD,
                            host="telegraph_bot_db",
                            port=5432)
    curs = conn.cursor()
    return curs


class DBTokensHandler:
    @staticmethod
    def update_me(message: types.Message) -> str:
        """Set new token for User if one exists.

        Args:
            message: Message object.

        Returns:
            User token.

        """
        curs = cur()
        uid = message.from_user.id
        token = abs(hash(str(uid - message.id + message.date)))
        curs.execute("UPDATE users SET username = %s, user_token = %s WHERE user_id = %s",
                     [
                           message.from_user.username,
                           token,
                           uid
                       ])
        curs.connection.commit()
        curs.connection.close()
        return str(token)

    @staticmethod
    def set_me(message: types.Message) -> str:
        """Set new token for User if none exists.

        Args:
            message: Message object.

        Returns:
            User token.

        """
        curs = cur()
        uid = message.from_user.id
        token = abs(hash(str(uid - message.id + message.date)))
        curs.execute("INSERT INTO users (username, user_id, user_token) VALUES (%s, %s, %s)",
                     [
                           message.from_user.username,
                           uid,
                           token
                       ])
        curs.connection.commit()
        curs.connection.close()
        return str(token)

    @staticmethod
    def get_me(message: types.Message) -> str | None:
        """Get User token from the DB.

        Args:
            message: Message object.

        Returns:
            User token if exists, None otherwise.

        """
        curs = cur()
        uid = message.from_user.id
        curs.execute("SELECT user_token FROM users WHERE users.user_id = %s", [uid])
        token = curs.fetchone()
        curs.connection.close()
        return token[0] if token else None

    @classmethod
    def set_recipient(cls, message: types.Message) -> str:
        """Set new Recipient token for User.

        Args:
            message: Message object from User with new token in it.

        Returns:
            New Recipient token.

        """
        curs = cur()
        if not cls.get_me(message):
            cls.set_me(message)
        token = message.text
        for symbol in token:
            if not symbol.isdigit():
                token = token.replace(symbol, '')
        curs.execute("UPDATE users SET current_recipient = %s WHERE user_id = %s",
                     [
                           token,
                           message.from_user.id
                       ])
        curs.connection.commit()
        curs.connection.close()
        return str(token)

    @classmethod
    def set_random_recipient(cls, message: types.Message) -> str | None:
        """Set random Recipient token from existing tokens in the DB except User's one.

        Args:
            message: Message object.

        Returns:
            New Recipient token if set, otherwise None.

        """
        curs = cur()
        if not cls.get_me(message):
            cls.set_me(message)
        curs.execute("SELECT user_token FROM users WHERE users.user_id != %s",
                     [message.from_user.id])
        tokens = curs.fetchall()
        if tokens:
            token = tokens[random.randint(0, len(tokens) - 1)]
            curs.execute("UPDATE users SET current_recipient = %s WHERE user_id = %s",
                         [
                               token,
                               message.from_user.id
                           ])
            curs.connection.commit()
            curs.connection.close()
            return str(token[0])
        curs.connection.close()
        return None

    @classmethod
    def get_recipient(cls, message: types.Message) -> str | None:
        """Get Recipient token from the DB.

        Args:
            message: Message object.

        Returns:
            Recipient token if exists, None otherwise.

        """
        curs = cur()
        if not cls.get_me(message):
            cls.set_me(message)
        uid = message.from_user.id
        curs.execute("SELECT current_recipient FROM users WHERE user_id = %s", [uid])
        recipient = curs.fetchone()
        curs.connection.close()
        return recipient[0] if recipient else None

    @classmethod
    def delete_recipient(cls, message: types.Message) -> None:
        """Delete Recipient token form the DB.

        Args:
            message: Message object.

        """
        curs = cur()
        if not cls.get_me(message):
            cls.set_me(message)
        curs.execute("UPDATE users SET current_recipient = null WHERE user_id = %s",
                     [message.from_user.id])
        curs.connection.commit()
        curs.connection.close()

    @classmethod
    def get_recipient_id(cls, message: types.Message) -> int | None:
        """Get Recipient ID form the DB.

        Args:
            message: Message object.

        Returns:
            Recipient ID if found, None otherwise.

        """
        curs = cur()
        if not cls.get_me(message):
            cls.set_me(message)
        recipient = cls.get_recipient(message)
        if recipient:
            curs.execute("SELECT user_id FROM users WHERE user_token = %s", [recipient])
            recipient_id = curs.fetchone()
            curs.connection.close()
            return recipient_id[0] if recipient_id else None
        curs.connection.close()
        return None
