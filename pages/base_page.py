import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select

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

    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Element not visible: {str(e)}")
            return False

    def select_by_value(self, locator, value):
        """Select dropdown option by value"""
        try:
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_value(value)
            return True
        except Exception as e:
            self.logger.error(f"Failed to select value {value}: {str(e)}")
            return False
