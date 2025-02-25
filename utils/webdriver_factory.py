from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
from functools import lru_cache

class WebDriverFactory:
    @classmethod
    @lru_cache(maxsize=1)  # Cache ChromeDriver installation
    def _get_driver_path(cls):
        """Cache the ChromeDriver path to avoid repeated downloads"""
        return ChromeDriverManager().install()

    @classmethod
    def get_driver(cls):
        """Get optimized WebDriver instance"""
        try:
            # Silence WDM and Selenium logging
            logging.getLogger('WDM').setLevel(logging.ERROR)
            logging.getLogger('selenium').setLevel(logging.ERROR)
            
            chrome_options = webdriver.ChromeOptions()
            # Essential options only
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--log-level=3')  # Minimal Chrome logging
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            
            service = Service(
                cls._get_driver_path(),
                log_path=None  # Disable service logging
            )
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(30)  # Set page load timeout
            driver.implicitly_wait(5)  # Set implicit wait
            
            return driver

        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {str(e)}")
            raise

    @staticmethod
    def create_driver(browser_type="chrome"):
        """Create WebDriver instance with configured options"""
        logger = logging.getLogger(__name__)
        
        if browser_type.lower() == "chrome":
            try:
                # Set up Chrome options
                chrome_options = Options()
                chrome_options.add_argument('--start-maximized')
                chrome_options.add_argument('--disable-extensions')
                chrome_options.add_argument('--disable-notifications')
                
                # Disable password saving and autofill
                prefs = {
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                    "profile.default_content_setting_values.notifications": 2,
                    "autofill.profile_enabled": False,
                    "profile.password_manager_enabled": False,
                    "profile.default_content_settings.popups": 0
                }
                chrome_options.add_experimental_option("prefs", prefs)
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                
                # Initialize driver with options
                driver = webdriver.Chrome(options=chrome_options)
                logger.info("Chrome WebDriver created successfully")
                return driver
                
            except Exception as e:
                logger.error(f"Failed to create Chrome WebDriver: {str(e)}")
                raise
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
