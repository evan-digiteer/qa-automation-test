from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import logging
from functools import lru_cache
from time import time

class WebDriverFactory:
    @classmethod
    @lru_cache(maxsize=1)  # Cache ChromeDriver installation
    def _get_driver_path(cls):
        """Cache the ChromeDriver path to avoid repeated downloads"""
        return ChromeDriverManager().install()

    @staticmethod
    def clear_cache():
        """Clear the driver path cache to force new download"""
        WebDriverFactory._get_driver_path.cache_clear()

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
            chrome_options.add_argument('--disable-gpu')  
            chrome_options.add_argument('--disable-extensions')  
            chrome_options.add_argument('--disable-infobars')  
            chrome_options.add_argument('--disable-notifications')  
            chrome_options.add_argument('--disable-default-apps')  
            chrome_options.add_argument('--dns-prefetch-disable')  
            chrome_options.add_argument('--page-load-strategy=eager')  
            
            # Logging optimizations
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Performance preferences
            chrome_options.add_experimental_option('prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0,
                'profile.default_content_setting_values.automatic_downloads': 1,
                'profile.default_content_setting_values.geolocation': 2,
                'profile.managed_default_content_settings.images': 1,  
                'profile.default_content_setting_values.cookies': 1
            })
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)  
            driver.implicitly_wait(5) 
            
            return driver

        except Exception as e:
            logging.error(f"Failed to initialize WebDriver: {str(e)}")
            raise
