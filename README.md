# Jobot
A python bot to list jobs and apply to Linkedin jobs and notify you using a telegram bot.

# Getting Started
    Telegram Setup:
        1- Go to [@BotFather](https://t.me/botfather).
        2- Type /newbot
        3- Add Bot name and username.
        4- Get <BOT-TOKEN>
        5- Create group chat and include your bot.
        6- Get ChatID by bot token `https://api.telegram.org/bot<YourBOTToken>/getUpdates`

## Installation
```console
$ git clone git@github.com:elmarzouki/jobot.git
$ python3 -m venv venv
$ pip install -r requirements.txt
$ cp .env.example .env
$ nano .env
$ python3 jobot.py
```
## Dockerized
```console
$ docker compose up --build -d
$ docker compose logs -f
```