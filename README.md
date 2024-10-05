# 📠 Telegraph Telegram bot

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

Token-based Telegram bot to anonymously chat with each other.

Bot is available [here](https://t.me/Seemann_ng_anonchat_bot)

## 💾 Build and run:

Run the following command to start the bot:

```bash
docker compose up -d --build
```

## 🔐 Environment:

In the `.env` file, or through the `-e` flags, you must set the required variables from
tables below.

| Variable       | Default         | Description                                  |
|----------------|-----------------|----------------------------------------------|
| `BOT_TOKEN`    | **(required)**  | Telegram bot token                           | 
| `DB_USER`      | **(required)**  | DB User name                                 |
| `DB_PASSWORD`  | **(required)**  | DB User password                             |
| `DB_EXT_PORT`  | **(required)**  | External DB host port, `5432` is recommended |


## 📠 Interaction with the bot:

### ⌨️ _Commands:_

`/start` - sends a welcome message to User and sets them new token.
 
`/new_token` - sets new token for User.

`/my_token` - sends User message with their token.

`/set_recipient` - sends User request for new Recipient's token. Replying to one sets new Recipient.
  
__⚠️ Bot only recognizes digits in the reply message.__

`/delete_recipient` - changes Recipient's token to null value, so messages aren't forwarded to any recipient.

`/get_recipient` - sends User message with current Recipient's token.

`/random_recipient` - connects User to random Recipient from the database.

__✉️ Once new User gets their User token and sets a known to them or random Recipient's token, every text message sent to the bot is being re-sent to corresponding Recipient only revealing User's token.__

## 👨‍🔧Built with:

* [Python 3.12](https://www.python.org/) - programming language.
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE from JetBrains.

## 👨‍💻 Author:

* **Ilia Tashkenov (_セーラー_)** - [Seemann-ng](https://github.com/Seemann-ng), 2024

## 📝 License:

This project is licensed under the MIT License - see the [license website](https://opensource.org/licenses/MIT) for details
