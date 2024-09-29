# 🤖 Jobot
A python bot to search linkedin jobs based on user preferences and notify back using telegram bot.

# 🚀 Getting Started
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

## 🔌 Installation
```console
# make sure that python 3.12 and pip is installed
$ git clone git@github.com:elmarzouki/jobot.git
$ cd jobot/
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
## 💡 Features
* Filter linkedin jobs by your preferences such as: location, keywords, experience, date_posted, job_type, remote, sort_by, and easy_apply
* Filter job description itself by your defined search keywords.
* Send telegram notifications on a predefined channel.
* Randomized time for actions taken and events window on your linkedin account to mimic the human interaction.
* Console logger to output bot actions.
## 🖥️ Demo 
![console sample logs](<img/console-sample.png>)
![telegram sample notifications](<img/tele-sample.png>)
