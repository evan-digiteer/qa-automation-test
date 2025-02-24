from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
            logging.getLogger('WDM').setLevel(logging.ERROR)
            
            chrome_options = webdriver.ChromeOptions()
            # Performance optimizations
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--disable-gpu')  # Reduce GPU usage
            chrome_options.add_argument('--disable-extensions')  # Disable extensions
            chrome_options.add_argument('--disable-infobars')  # Disable infobars
            chrome_options.add_argument('--disable-notifications')  # Disable notifications
            chrome_options.add_argument('--disable-default-apps')  # Disable default apps
            chrome_options.add_argument('--dns-prefetch-disable')  # Disable DNS prefetching
            chrome_options.add_argument('--page-load-strategy=eager')  # Don't wait for full page load
            
            # Logging optimizations
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Performance preferences
            chrome_options.add_experimental_option('prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0,
                'profile.default_content_setting_values.automatic_downloads': 1,
                'profile.default_content_setting_values.geolocation': 2,
                'profile.managed_default_content_settings.images': 1,  # 2 to disable images
                'profile.default_content_setting_values.cookies': 1
            })
            
            service = Service(
                cls._get_driver_path(),
                log_path='NUL'
            )
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(30)  # Set page load timeout
            driver.implicitly_wait(5)  # Set implicit wait
            
            return driver

        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {str(e)}")
            raise
