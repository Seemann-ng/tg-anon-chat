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

