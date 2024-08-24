import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL")
LN_EMAIL = os.getenv("LN_EMAIL")
LN_PASSWORD = os.getenv("LN_PASSWORD")
