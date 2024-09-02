import random
import time
from browsers.chrome_browser import ChromeBrowser

def get_browsing_time() -> int:
    """get random int number to mimic the human browsing time"""
    # TODO:// increase the time
    # return round(random.uniform(15, 60))
    return round(random.uniform(1, 4))

def __get_browsing_size(y_coord) -> int:
    return round(random.uniform(y_coord*2, int(y_coord*2.5)))

def scrolling(driver) -> None:
    """
    get dynamic random y coord for browsing screen size
    and get dynamic random int for browsing time
    and do actual scrolling event
    """
    y_coord = 400 # small screen size
    sleepy = 0 # scroll if less than 4 min
    while y_coord < 10000 and sleepy < 240:
        ChromeBrowser.scroll(driver, 400)
        sleeping = get_browsing_time()
        sleepy += sleeping
        time.sleep(sleeping)
        y_coord = __get_browsing_size(y_coord)