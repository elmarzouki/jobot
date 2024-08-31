import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

from browsers.chrome_browser import ChromeBrowser
from logger import Logger
from spiders.linkedin import config, constants

logger = Logger("jobot")


class LinkedinSpider:
    def __init__(self, easy_apply: bool = True):
        logger.info("🕷️ Linkedin spider starting...")
        self.browser: Chrome = ChromeBrowser().get_browser()
        self.urls: list[str] = []
        self.easy_apply: bool = easy_apply

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
        
        # Mapping preferences to their respective config and constant dictionaries
        preference_map = {
            "jt": (config.job_type, constants.job_type),
            "remote": (config.remote, constants.remote),
            "location": ([location], constants.location) if location else ([], {}),
            "experience": (config.experience, constants.experience),
            "date": (config.date_posted, constants.date_posted),
            "sort_by": (config.sort_by, constants.sort_by)
        }
        
        for preference in preferences:
            filter_list, constant = preference_map.get(preference, ([], {}))
            
            if not filter_list or not constant:
                continue  # Skip if no valid config or constant
            
            # Validate that the filter_list contains valid keys from the constant
            filter_list = [
                item
                for item in constant.get("1", constant).keys()
                if any(x in item for x in filter_list)
            ]
            
            if not filter_list:
                continue  # If no valid config, skip this filter

            for index, filter_item in enumerate(filter_list):
                try:
                    if index == 0:
                        # Use the first filter item from "1"
                        filter_str += constant["1"][filter_item]
                    else:
                        # Use subsequent filter items from "n"
                        filter_str += constant["n"][filter_item]
                except KeyError:
                    filter_str += constant.get(filter_item, "")
        
        return filter_str

    def __generate_apply_url(self) -> List[str]:
        urls: List[str] = []
        al: str = "f_AL=true&" if self.easy_apply else "" # easy_apply flag
        for location in config.location:
            for keyword in config.keywords:
                url = f"{constants.LN_JOB_SEARCH_URL}?{al}origin=JOB_SEARCH_PAGE_JOB_FILTER&keywords={keyword}{self.__filter(["jt", "location", "remote", "experience", "date", "sort_by"], location)}"
                urls.append(url)
        return urls

    def scrap_jobs(self) -> None:
        self.urls= self.__generate_apply_url()
        for url in self.urls:
            time.sleep(60)
            logger.info(f'Scraping jobs from: {url}')
            self.browser.get(url)
            try:
                total_jobs_found = self.browser.find_element(
                    By.XPATH,'//*[@class="jobs-search-results-list__subtitle"]').text
            except:
                logger.info('No job was found')
                continue # skip empty page
            logger.info(total_jobs_found)
            total_jobs_found = int(total_jobs_found.replace(' results', ''))

    def apply(self, job_link: str) -> None:
        pass
