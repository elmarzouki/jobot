import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome

from browsers.chrome_browser import ChromeBrowser
from logger import Logger
from spiders.linkedin import config, constants

from human import get_browsing_time, scrolling
from math import ceil

logger = Logger("jobot")


class LinkedinSpider:
    def __init__(self, easy_apply: bool = True):
        logger.info("🕷️ Linkedin spider starting...")
        self.driver = ChromeBrowser()
        self.browser: Chrome = self.driver.get_browser()
        self.urls: List[str] = []
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
            time.sleep(get_browsing_time())
            password_input.send_keys(password)
            time.sleep(get_browsing_time())
            # login_button.click()
            password_input.send_keys(Keys.ENTER)
            time.sleep(get_browsing_time())
        except:
            logger.error("Couldn't login to linkedin account!")

    def is_logged(self) -> bool:
        # check for div id="ember14" if feed is displayed
        self.browser.get(constants.LN_FEED_URL)
        scrolling(self.driver)
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

    def scrap_job(self, current_job_url) -> dict:
        self.browser.get(current_job_url)
        scrolling(self.driver)
        job_details: dict = {
            'job_title': '', 'job_details': '', 'company': ''}
        try:
            job_details['job_title'] = self.browser.find_element(
                By.CLASS_NAME, 'job-details-jobs-unified-top-card__job-title').text
            job_details['job_details'] = self.browser.find_element(
                By.CLASS_NAME, 'job-details-jobs-unified-top-card__primary-description-container').text
            job_details['company'] = self.browser.find_element(
                By.CLASS_NAME, 'job-details-jobs-unified-top-card__company-name').text
            logger.info(job_details)
        except:
            logger.error(f'Failed to fetch data of: {current_job_url}')
            return
        return job_details


    def scrap_jobs(self) -> None:
        self.urls = self.__generate_apply_url()
        for url in self.urls:
            time.sleep(get_browsing_time())
            logger.info(f'Scraping jobs from: {url}')
            self.browser.get(url)
            try:
                total_jobs_found = self.browser.find_element(
                    By.XPATH,'//*[@class="jobs-search-results-list__subtitle"]').text
                logger.info(total_jobs_found)
            except:
                logger.info('No job was found')
                continue # skip empty page
            total_jobs_found = int(total_jobs_found.replace(' results', ''))
            total_pages = ceil(total_jobs_found/constants.LN_JOBS_PER_PAGE)

            for page in range(total_pages):
                current_jobs_ctr = page*constants.LN_JOBS_PER_PAGE
                url += "&start="+ str(current_jobs_ctr)
                self.browser.get(url)
                scrolling(self.driver)
                # get current jobs
                jobs_ids: List[int] = [] # fetch all jobs_ids
                current_jobs = self.browser.find_elements(By.XPATH,'//li[@data-occludable-job-id]')
                for job in current_jobs:
                    job_id = job.get_attribute("data-occludable-job-id")
                    job_id = int(job_id.split(":")[-1])
                    jobs_ids.append(job_id)

                for job_id in jobs_ids: # start featching job post one by one
                    current_job_url = 'https://www.linkedin.com/jobs/view/' + str(job_id)
                    logger.info(f'Job found: {current_job_url}')
                    _ = self.scrap_job(current_job_url)


    def easy_apply(self) -> None:
        pass

    def apply(self) -> None:
        pass
