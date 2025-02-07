import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)

    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise Exception(f"Element {locator} not found")

    def find_elements(self, locator):
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            self.logger.warning(f"Elements {locator} not found")
            return []

    def click(self, locator):
        self.find_element(locator).click()

    def type(self, locator, text):
        self.find_element(locator).send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text
