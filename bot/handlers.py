import random

import psycopg2
import telebot.types as types
from environs import Env

env = Env()
env.read_env()

DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")


def cursor(func):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(database="postgres",
                                user=DB_USER,
                                password=DB_PASSWORD,
                                host="database",
                                port=5432)
        curs = conn.cursor()
        result = func(*args, **kwargs, curs=curs)
        conn.commit()
        conn.close()
        return result

    return wrapper


class DBTokensHandler:
    @staticmethod
    @cursor
    def update_me(message: types.Message, curs: psycopg2.extensions.cursor) -> str:
        """Set new token for User if one exists.

        Args:
            message: Message object.
            curs: PostgreSQL cursor object.

        Returns:
            User token.

        """
        uid = message.from_user.id
        token = abs(hash(str(uid - message.id + message.date)))
        curs.execute("UPDATE users SET username = %s, user_token = %s WHERE user_id = %s",
                     (message.from_user.username, token, uid))
        return str(token)

    @staticmethod
    @cursor
    def set_me(message: types.Message, curs: psycopg2.extensions.cursor) -> str:
        """Set new token for User if none exists.

        Args:
            message: Message object.
            curs: PostgreSQL cursor object.

        Returns:
            User token.

        """
        uid = message.from_user.id
        token = abs(hash(str(uid - message.id + message.date)))
        curs.execute("INSERT INTO users (username, user_id, user_token) VALUES (%s, %s, %s)",
                     (message.from_user.username, uid, token))
        return str(token)

    @staticmethod
    @cursor
    def get_me(message: types.Message, curs: psycopg2.extensions.cursor) -> str:
        """Get User token from the DB.

        Args:
            message: Message object.
            curs: PostgreSQL cursor object.

        Returns:
            User token if exists, "" otherwise.

        """
        uid = message.from_user.id
        curs.execute("SELECT user_token FROM users WHERE users.user_id = %s", (uid, ))
        token = curs.fetchone()
        return token[0] if token else ""

    @classmethod
    @cursor
    def set_recipient(cls, message: types.Message, curs: psycopg2.extensions.cursor) -> str:
        """Set new Recipient token for User.

        Args:
            message: Message object from User with new token in it.
            curs: PostgreSQL cursor object.

        Returns:
            New Recipient token.

        """
        if not cls.get_me(message):
            cls.set_me(message)
        token = ''.join([symbol for symbol in message.text if symbol.isdigit()])
        curs.execute("UPDATE users SET current_recipient = %s WHERE user_id = %s",
                     (token, message.from_user.id))
        return str(token)

    @classmethod
    @cursor
    def set_random_recipient(cls, message: types.Message, curs: psycopg2.extensions.cursor) -> str:
        """Set random Recipient token from existing tokens in the DB except User's one.

        Args:
            message: Message object.
            curs: PostgreSQL cursor object.

        Returns:
            New Recipient token if set, otherwise "".

        """
        if not cls.get_me(message):
            cls.set_me(message)
        curs.execute("SELECT user_token FROM users WHERE users.user_id != %s",
                     (message.from_user.id, ))
        if tokens := curs.fetchall():
            token = tokens[random.randint(0, len(tokens) - 1)]
            curs.execute("UPDATE users SET current_recipient = %s WHERE user_id = %s",
                         (token, message.from_user.id))
            return str(token[0])
        return ""

    @classmethod
    @cursor
    def get_recipient(cls, message: types.Message, curs: psycopg2.extensions.cursor) -> str:
        """Get Recipient token from the DB.

        Args:
            message: Message object.
            curs: PostgreSQL cursor object.

        Returns:
            Recipient token if exists, "" otherwise.

        """
        if not cls.get_me(message):
            cls.set_me(message)
        uid = message.from_user.id
        curs.execute("SELECT current_recipient FROM users WHERE user_id = %s", (uid, ))
        recipient = curs.fetchone()
        return recipient[0] if recipient else ""

    @classmethod
    @cursor
    def delete_recipient(cls, message: types.Message, curs: psycopg2.extensions.cursor) -> None:
        """Delete Recipient token form the DB.

        Args:
            message: Message object.
            curs: PostgreSQL cursor object.

        """
        if not cls.get_me(message):
            cls.set_me(message)
        curs.execute("UPDATE users SET current_recipient = null WHERE user_id = %s",
                     (message.from_user.id, ))

    @classmethod
    @cursor
    def get_recipient_id(cls, message: types.Message, curs: psycopg2.extensions.cursor) -> int:
        """Get Recipient ID form the DB.

        Args:
            message: Message object.
            curs: PostgreSQL cursor object.

        Returns:
            Recipient ID if found, 0 otherwise.

        """
        if not cls.get_me(message):
            cls.set_me(message)
        if recipient := cls.get_recipient(message):
            curs.execute("SELECT user_id FROM users WHERE user_token = %s", (recipient, ))
            recipient_id = curs.fetchone()
            return recipient_id[0] if recipient_id else 0
        return 0
