import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from browsers.chrome_browser import ChromeBrowser
from logger import Logger
from spiders.linkedin import config, constants

logger = Logger("jobot")


class LinkedinSpider:
    def __init__(self):
        logger.info("🕷️ Linkedin spider starting...")
        self.browser = ChromeBrowser().get_browser()

    def login(self, username: str, password: str) -> None:
        logger.info("Logging in...")
        self.browser.get(constants.LN_LOGIN_URL)
        try:
            email_input = self.browser.find_element(By.ID, "username")
            password_input = self.browser.find_element(By.ID, "password")
            # login_button = self.browser.find_element("xpath",
            #             '//*[@id="organic-div"]/form/div[3]/button')
            email_input.send_keys(username)
            time.sleep(2)
            password_input.send_keys(password)
            time.sleep(2)
            # login_button.click()
            password_input.send_keys(Keys.ENTER)
            time.sleep(30)
        except:
            logger.error("Couldn't login to linkedin account!")

    def is_logged(self) -> bool:
        # check for div id="ember14" if feed is displayed
        self.browser.get(constants.LN_FEED_URL)
        try:
            self.browser.find_element(By.XPATH, '//*[@id="ember14"]')
            return True
        except:
            return False

    def __filter(self, preferences: List[str], location: str = None) -> str:
        filter_str: str = ""
        for preference in preferences:
            # define filter list from config and constants list
            # to load search strings
            filter_list: List[str] = []
            constant: dict = {}
            # init vars
            if preference == "jt":
                filter_list = config.job_type
                constant = constants.job_type
            elif preference == "remote":
                filter_list = config.remote
                constant = constants.remote
            elif preference == "location":
                filter_list = [location]
                constant = constants.location
            elif preference == "experience":
                filter_list = config.experience
                constant = constants.experience
            elif preference == "date":
                filter_list = config.date_posted
                constant = constants.date_posted
            elif preference == "sort_by":
                filter_list = config.sort_by
                constant = constants.sort_by
            # validate that the passed list in config matches the constants
            filter_list = [
                item
                for item in constant["1"].keys()
                if any(x in item for x in filter_list)
            ]
            if not filter_list:
                continue  # if not valid config skip filter
            for index in range(0, len(filter_list)):
                if index == 0:
                    try:
                        # filter with neasted dicts
                        filter_str += constant["1"][filter_list[index]]
                    except:
                        filter_str += constant[filter_list[index]]
                else:
                    filter_str += constant["n"][filter_list[index]]
        return filter_str

    def generate_apply_url(self) -> List[str]:
        path: List[str] = []
        for location in config.location:
            for keyword in config.keywords:
                url = f"{constants.LN_JOB_SEARCH_URL}?f_AL=true&keywords={keyword}{self.__filter(["jt", "remote", "location", "experience", "date", "sort_by"], location)}"
                path.append(url)
        return path

    def scrap_jobs(self) -> None:
        pass
