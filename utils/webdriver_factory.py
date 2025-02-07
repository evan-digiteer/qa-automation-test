from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging

class WebDriverFactory:
    @classmethod
    def get_driver(cls):
        """Get WebDriver instance"""
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--ignore-certificate-errors')
            
            # Use ChromeDriverManager's built-in caching
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver

        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {str(e)}")
            raise
