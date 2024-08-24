import asyncio
import time

from constants import LN_EMAIL, LN_PASSWORD
from logger import Logger
from spiders.linkedin.linkedin_spider import LinkedinSpider

logger = Logger("jobot")


def main() -> None:
    logger.info("🤖 Jobot starting...")

    # try:
    spider = LinkedinSpider()
    spider.login(username=LN_EMAIL, password=LN_PASSWORD)
    time.sleep(15)
    spider.is_logged()
    # except:
    # logger.error("Jobot stoped..")

    # Create a new event loop if none exists
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:  # If no loop is running, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Let the loop run for a short time to allow tasks to complete
    loop.run_until_complete(asyncio.sleep(0.1))

    # Close the loop
    loop.close()


if __name__ == "__main__":
    main()
