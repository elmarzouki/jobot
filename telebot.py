from telegram import Bot

from constants import TELEGRAM_CHANNEL, TELEGRAM_TOKEN


async def notify(message: str) -> None:
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHANNEL, text=message)
