import asyncio
import logging

from colorlog import ColoredFormatter

from telebot import notify


class Logger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.extra_info = None
        handler = logging.StreamHandler()
        LOGFORMAT = " %(log_color)s%(asctime)s%(reset)s | %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
        formatter = ColoredFormatter(LOGFORMAT)
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def notify(self, msg, *args, xtra=None, **kwargs):
        extra_info = xtra if xtra is not None else self.extra_info
        self._schedule_notify(msg)
        super().info(msg, *args, extra=extra_info, **kwargs)

    def info(self, msg, *args, xtra=None, **kwargs):
        extra_info = xtra if xtra is not None else self.extra_info
        super().info(msg, *args, extra=extra_info, **kwargs)

    def error(self, msg, *args, xtra=None, **kwargs):
        extra_info = xtra if xtra is not None else self.extra_info
        super().error(msg, *args, extra=extra_info, **kwargs)

    def debug(self, msg, *args, xtra=None, **kwargs):
        extra_info = xtra if xtra is not None else self.extra_info
        super().debug(msg, *args, extra=extra_info, **kwargs)

    def _schedule_notify(self, msg):
        # Ensure that the event loop is running and schedule the task
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(self._notify(msg))
        else:
            loop.run_until_complete(self._notify(msg))

    async def _notify(self, msg):
        await notify(msg)
