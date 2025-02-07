from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class WebDriverFactory:
    @staticmethod
    def get_driver(browser_name='chrome'):
        if browser_name.lower() == 'chrome':
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service)
        elif browser_name.lower() == 'firefox':
            service = Service(GeckoDriverManager().install())
            return webdriver.Firefox(service=service)
        else:
            raise ValueError(f"Browser {browser_name} is not supported")
