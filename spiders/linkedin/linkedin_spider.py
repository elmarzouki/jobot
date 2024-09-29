import time
from math import ceil
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browsers.chrome_browser import ChromeBrowser
from config import linkedin_conf
from human import get_browsing_time, scrolling
from logger import Logger
from spiders.linkedin import constants

logger = Logger("jobot")


class LinkedinSpider:
    def __init__(self):
        logger.notify("🕷️ Linkedin spider starting...")
        # init vars
        self.driver = ChromeBrowser()
        self.browser: Chrome = self.driver.get_browser()
        self.urls: List[str] = []
        self.easy_apply: bool = linkedin_conf.easy_apply
        self.search_tokens: List[str] = linkedin_conf.search_tokens
        self.account_cookie: str = ""
        # laod cookies
        self.browser.get(constants.LN_URL)
        self.driver.load_cookies(self.account_cookie)
        if not self.is_logged():
            from constants import LN_EMAIL, LN_PASSWORD

            self.login(username=LN_EMAIL, password=LN_PASSWORD)
            time.sleep(get_browsing_time())

        self.scrap_jobs()

    def login(self, username: str, password: str) -> None:
        logger.info("Logging in...")
        self.browser.get(constants.LN_LOGIN_URL)
        try:
            email_input = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_input = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            email_input.send_keys(username)
            time.sleep(get_browsing_time())
            password_input.send_keys(password)
            time.sleep(get_browsing_time())
            password_input.send_keys(Keys.ENTER)
            time.sleep(get_browsing_time())
            # save a cookie
            self.account_cookie = self.driver.new_cookie(username)
        except:
            logger.error("Couldn't login to linkedin account!")

    def is_logged(self) -> bool:
        # check for div id="ember14" if feed is displayed
        self.browser.get(constants.LN_FEED_URL)
        scrolling(self.driver)
        try:
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ember14"]'))
            )
            return True
        except:
            return False

    def __filter(self, preferences: List[str], location: str = None) -> str:
        filter_str: str = ""

        # Mapping preferences to their respective config and constant dictionaries
        preference_map = {
            "jt": (linkedin_conf.job_type, constants.job_type),
            "remote": (linkedin_conf.remote, constants.remote),
            "location": ([location], constants.location) if location else ([], {}),
            "experience": (linkedin_conf.experience, constants.experience),
            "date": (linkedin_conf.date_posted, constants.date_posted),
            "sort_by": (linkedin_conf.sort_by, constants.sort_by),
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
        al: str = "f_AL=true&" if self.easy_apply else ""  # easy_apply flag
        for location in linkedin_conf.location:
            for keyword in linkedin_conf.keywords:
                url = f"{constants.LN_JOB_SEARCH_URL}?{al}origin=JOB_SEARCH_PAGE_JOB_FILTER&keywords={keyword}{self.__filter(["jt", "location", "remote", "experience", "date", "sort_by"], location)}"
                urls.append(url)
        return urls

    def scrap_job(self, current_job_url: str) -> dict:
        job_details: dict = {"job_title": "", "job_details": "", "company": ""}
        self.browser.get(current_job_url)
        scrolling(self.driver)
        try:
            job_description = self.browser.find_element(
                By.CLASS_NAME, "jobs-description-content__text"
            ).text
        except NoSuchElementException:
            logger.error(f"Job description was not found at: {current_job_url}")
            return job_details
        found_tokens: List[str] = list(
            filter(lambda s: s in job_description, self.search_tokens)
        )
        # if self.search_tokens and len(found_tokens) != len(self.search_tokens):
        if not found_tokens:
            logger.error(f"Search tokens was not found at: {current_job_url}")
            return job_details
        try:
            job_details["job_title"] = (
                WebDriverWait(self.browser, 10)
                .until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title")
                    )
                )
                .text
            )
            job_details["job_details"] = (
                WebDriverWait(self.browser, 10)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.CLASS_NAME,
                            "job-details-jobs-unified-top-card__primary-description-container",
                        )
                    )
                )
                .text
            )
            job_details["company"] = (
                WebDriverWait(self.browser, 10)
                .until(
                    EC.presence_of_element_located(
                        (
                            By.CLASS_NAME,
                            "job-details-jobs-unified-top-card__company-name",
                        )
                    )
                )
                .text
            )
            logger.notify(job_details)
            logger.notify(current_job_url)
        except NoSuchElementException as e:
            logger.error(f"Failed to fetch data at: {current_job_url}: {str(e)}")
        return job_details

    def scrap_jobs(self) -> None:
        self.urls = self.__generate_apply_url()
        for url in self.urls:
            time.sleep(get_browsing_time())
            logger.info(f"Scraping jobs from: {url}")
            self.browser.get(url)
            try:
                total_jobs_found = (
                    WebDriverWait(self.browser, 10)
                    .until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "jobs-search-results-list__subtitle")
                        )
                    )
                    .text
                )
                total_jobs_found = int(total_jobs_found.replace(" results", "").replace(" result", ""))
                logger.info(f"Total jobs found: {total_jobs_found}")
            except NoSuchElementException:
                logger.info("No job was found")
                continue  # skip empty page
            except Exception as e:
                logger.error(f"Error fetching total jobs: {str(e)}")
                continue

            total_pages = ceil(total_jobs_found / constants.LN_JOBS_PER_PAGE)

            for page in range(total_pages):
                current_jobs_ctr = page * constants.LN_JOBS_PER_PAGE
                paginated_url = f"{url}&start={current_jobs_ctr}"
                logger.info(
                    f"Scraping page {page + 1} / {total_pages}: {paginated_url}"
                )
                self.browser.get(paginated_url)
                scrolling(self.driver)
                # get current jobs
                jobs_ids: List[int] = []  # fetch all jobs_ids
                try:
                    current_jobs = self.browser.find_elements(
                        By.XPATH, "//li[@data-occludable-job-id]"
                    )
                    for job in current_jobs:
                        job_id = job.get_attribute("data-occludable-job-id")
                        job_id = int(job_id.split(":")[-1])
                        jobs_ids.append(job_id)
                except NoSuchElementException:
                    logger.error("No job elements found on page")
                    continue
                except Exception as e:
                    logger.error(f"Error fetching job IDs: {str(e)}")
                    continue
                for job_id in jobs_ids:  # start featching job post one by one
                    current_job_url = f"https://www.linkedin.com/jobs/view/{job_id}"
                    logger.info(f"Job found: {current_job_url}")
                    _ = self.scrap_job(current_job_url)

    def easy_apply(self) -> None:
        pass

    def apply(self) -> None:
        pass
