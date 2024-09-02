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

    def scroll(self, y_coord) -> None:
        self.browser.execute_script("window.scrollTo(0," + str(y_coord) + " );")