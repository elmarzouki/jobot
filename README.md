# Jobot
A python bot to search linkedin jobs based on user preferences and notify back using telegram bot.

# Getting Started
    Telegram Setup:
        1- Go to [@BotFather](https://t.me/botfather).
        2- Type /newbot
        3- Add Bot name and username.
        4- Get <BOT-TOKEN>
        5- Create group chat and include your bot.
        6- Get ChatID by bot token `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
    Linkedin:
        1- this app version dose not support 2FA.
        2- so for the first time setup login to linked from you current device.

## Installation
```console
$ git clone git@github.com:elmarzouki/jobot.git
$ python3 -m venv venv
$ pip install -r requirements.txt
$ cp .env.example .env
$ nano .env # to add your telegram and linkedin credentials
$ nano config/linkedin_conf.py # make sure you update it with your preferences
$ python3 jobot.py
```
## Dockerized
```console
$ docker compose up --build -d
$ docker compose logs -f
```