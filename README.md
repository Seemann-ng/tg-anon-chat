# 📠 'Telegraph' Telegram bot 📠

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

#### _Token-based Telegram bot to anonymously chat with each other._

> ___Bot is available on https://t.me/Seemann_ng_anonchat_bot___

----

## 💾 Deployment: 💾

- __Insert Your database container name, postgres username and password in the corresponding fields:\
`container_name`, `POSTGRES_USER` and `POSTGRES_PASSWORD` of the `bot_db` service in the `docker-compose.yml` file.__

  - ___Optionally You can change port settings in the `ports` field.___
  
    ⚠️ _Note: the port after ':' symbol must be same as in `credentials.py`._
  
- __Insert Your bot container name and bot image name in the `container_name` and `image` fields of the `bot` service\
in the `docker-compose.yml` file.__

- __Insert Your bot token into field `"BOT_TOKEN"` in `credentials.py`.__

- __Fill `DB_USER`, `DB_PASSWORD` (and `DB_PORT` if changed) fields as per `docker-compose.yml`.__

- __Run `Docker Engine`.__

- __Execute the following commands from the project directory:__

  - ```bash
    docker image build . -t BOT-IMAGE-NAME
    ```
  
  ⚠️ ___`BOT-IMAGE-NAME` must be as per `docker-compose.yml`.___

  - ```bash
    docker compose -f docker-compose.yml up -d --force-recreate
    ```
    
----

## 📠 Interaction with the bot: 📠

### ⌨️ _Commands:_ ⌨️

`/start` __- sends a welcome message to User and sets them new token.__
 
`/new_token` __- sets new token for User.__

`/my_token` __- sends User message with their token.__

`/set_recipient` __- sends User request for new Recipient's token. Replying to one sets new Recipient.__
  
__⚠️ Bot only recognizes digits in the reply message.__

`/delete_recipient` __- changes Recipient's token to null value, so messages aren't forwarded to any recipient.__

`/get_recipient` __- sends User message with current Recipient's token.__

`/random_recipient` __- connects User to random Recipient from the database.__

__✉️ Once new User gets their User token and sets a known to them or random Recipient's token, every text message sent to the bot is being re-sent to corresponding Recipient only revealing User's token.__