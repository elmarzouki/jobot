import pickle
import hashlib
from os import path, getcwd, makedirs
from selenium import webdriver


class ChromeBrowser:
    def __init__(self) -> None:
        self.browser = webdriver.Chrome(
            options=self.__get_browser_options(),
        )

    def __get_browser_options(self) -> dict:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--incognito")
        return options

    def get_browser(self) -> webdriver.Chrome:
        return self.browser

    def scroll(self, y_coord: int) -> None:
        self.browser.execute_script("window.scrollTo(0," + str(y_coord) + " );")

    def new_cookie(self, hash_name: str) -> str:
        hash: str = hashlib.md5(hash_name.encode('utf-8')).hexdigest()
        base_path: str = path.join(getcwd(),'cookies/')
        makedirs(path.dirname(base_path), exist_ok=True)
        cookie_path: str = f"{base_path}/{hash}.pkl"
        pickle.dump(self.browser.get_cookies() , open(cookie_path,"wb"))
        return cookie_path

    def load_cookies(self, cookies_path: str) -> None:
        if path.exists(cookies_path):
            cookies = pickle.load(open(cookies_path, "rb"))
            self.browser.delete_all_cookies()
            for cookie in cookies:
                self.browser.add_cookie(cookie)
        