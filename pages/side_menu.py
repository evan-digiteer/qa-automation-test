from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .base_page import BasePage

class SideMenu(BasePage):
    # Update locators to use exact text matches
    DASHBOARD_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="Dashboard"]/parent::a')
    CONTENT_BANNER_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="Content & Banner"]/parent::a')
    PRODUCT_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="Product"]/parent::a')
    STORE_BRANCHES_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="Store Branches"]/parent::a')
    ANNOUNCEMENTS_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="News & Announcements"]/parent::a')
    CAREERS_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="Careers"]/parent::a')
    ROLES_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="Roles"]/parent::a')
    USERS_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="Users"]/parent::a')
    LOGS_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link")]//span[text()="Logs"]/parent::a')
    
    # Collapsible buttons
    SYSTEM_SETTINGS_BUTTON = (By.XPATH, '//button[@aria-controls="collapseSystemSettings"]//span[text()="System Settings"]/parent::button')
    INQUIRIES_BUTTON = (By.XPATH, '//button[@aria-controls="collapseInquiries"]//span[text()="Inquiries"]/parent::button')
    
    # Submenu sections - Used for checking expansion
    SYSTEM_SETTINGS_SECTION = (By.ID, 'collapseSystemSettings')
    INQUIRIES_SECTION = (By.ID, 'collapseInquiries')
    
    # Submenu items - Updated with exact paths
    CATEGORIES_LINK = (By.XPATH, '//div[@id="collapseSystemSettings"]//a[contains(@class, "sidebar__link--sub")]//span[text()="Categories"]/parent::a')
    AREAS_LINK = (By.XPATH, '//div[@id="collapseSystemSettings"]//a[contains(@class, "sidebar__link--sub")]//span[text()="Areas"]/parent::a')
    ANNOUNCEMENT_CATEGORIES_LINK = (By.XPATH, '//div[@id="collapseSystemSettings"]//a[contains(@class, "sidebar__link--sub")]//span[text()="News & Announcements Categories"]/parent::a')
    MESSAGES_LINK = (By.XPATH, '//div[@id="collapseInquiries"]//a[contains(@class, "sidebar__link--sub")]//span[text()="Messages"]/parent::a')
    FUNCTION_ROOM_LINK = (By.XPATH, '//div[@id="collapseInquiries"]//a[contains(@class, "sidebar__link--sub")]//span[text()="Function Room"]/parent::a')
    
    def wait_for_sidebar_load(self):
        """Wait for sidebar to be fully loaded"""
        try:
            # Wait for page load first
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            # Then wait for sidebar elements with longer timeout
            long_wait = WebDriverWait(self.driver, 20)
            long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar")))
            long_wait.until(EC.visibility_of_element_located(self.HEADER_LOGO))
            return True
        except Exception as e:
            self.logger.error(f"Sidebar failed to load: {str(e)}")
            return False

    def expand_submenu(self, button_locator, expected_submenu_id):
        """Generic method to expand submenu"""
        try:
            # Wait for button with longer timeout
            long_wait = WebDriverWait(self.driver, 15)
            button = long_wait.until(EC.element_to_be_clickable(button_locator))
            
            # Check if already expanded
            submenu = self.driver.find_element(By.ID, expected_submenu_id)
            if 'show' not in submenu.get_attribute('class'):
                # Click using JavaScript
                self.driver.execute_script("arguments[0].click();", button)
                # Wait for expansion
                long_wait.until(
                    lambda d: 'show' in d.find_element(By.ID, expected_submenu_id).get_attribute('class')
                )
            return True
        except Exception as e:
            self.logger.error(f"Failed to expand submenu: {str(e)}")
            return False

    def is_submenu_expanded(self, submenu_id):
        """Check if submenu is expanded"""
        try:
            section = self.find_element((By.ID, f"collapse{submenu_id.title()}"))
            return 'show' in section.get_attribute('class')
        except Exception as e:
            self.logger.error(f"Error checking submenu expansion: {str(e)}")
            return False

    def wait_for_submenu_visibility(self, submenu_id):
        """Wait for submenu section to be visible"""
        try:
            section = self.wait.until(
                EC.visibility_of_element_located((By.ID, submenu_id))
            )
            return 'show' in section.get_attribute('class')
        except Exception as e:
            self.logger.error(f"Error waiting for submenu visibility: {str(e)}")
            return False

    def expand_system_settings(self):
        """Expand System Settings submenu"""
        try:
            # Click only if not already expanded
            submenu = self.find_element(self.SYSTEM_SETTINGS_SECTION)
            if 'show' not in submenu.get_attribute('class'):
                # Use JavaScript click for reliability
                button = self.find_element(self.SYSTEM_SETTINGS_BUTTON)
                self.driver.execute_script("arguments[0].click();", button)
                # Wait for animation to complete
                self.wait.until(lambda d: 'show' in submenu.get_attribute('class'))
            
            # Verify submenu items are visible
            self.wait.until(
                EC.visibility_of_element_located(self.CATEGORIES_LINK)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to expand System Settings: {str(e)}")
            return False

    def expand_inquiries(self):
        """Expand Inquiries submenu"""
        try:
            # Click only if not already expanded
            submenu = self.find_element(self.INQUIRIES_SECTION)
            if 'show' not in submenu.get_attribute('class'):
                # Use JavaScript click for reliability
                button = self.find_element(self.INQUIRIES_BUTTON)
                self.driver.execute_script("arguments[0].click();", button)
                # Wait for animation to complete
                self.wait.until(lambda d: 'show' in submenu.get_attribute('class'))
            
            # Verify submenu items are visible
            self.wait.until(
                EC.visibility_of_element_located(self.MESSAGES_LINK)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to expand Inquiries: {str(e)}")
            return False

    def click_link_with_retry(self, locator, expected_url_part):
        """Click link with retry mechanism"""
        try:
            long_wait = WebDriverWait(self.driver, 15)
            element = long_wait.until(EC.element_to_be_clickable(locator))
            
            # First try normal click
            try:
                element.click()
            except:
                # If normal click fails, try JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
            
            # Wait for URL change
            long_wait.until(lambda d: expected_url_part in d.current_url.lower())
            return True
        except Exception as e:
            self.logger.error(f"Failed to click link: {str(e)}")
            return False

    # Update other navigation methods to use click_link_with_retry
    def navigate_to_section(self, section):
        """Navigate to a main section of the sidebar"""
        try:
            section_mapping = {
                'dashboard': (self.DASHBOARD_LINK, '/admin/dashboard'),
                'content': (self.CONTENT_BANNER_LINK, '/admin/content-and-banner'),
                'product': (self.PRODUCT_LINK, '/admin/products'),
                'store_branches': (self.STORE_BRANCHES_LINK, '/admin/store-branches'),
                'announcements': (self.ANNOUNCEMENTS_LINK, '/admin/announcements'),
                'careers': (self.CAREERS_LINK, '/admin/careers'),
                'roles': (self.ROLES_LINK, '/admin/roles'),
                'users': (self.USERS_LINK, '/admin/users'),
                'logs': (self.LOGS_LINK, '/admin/audittrails')
            }
            
            if section not in section_mapping:
                raise ValueError(f"Unknown section: {section}")
                
            locator, expected_url = section_mapping[section]
            
            # Wait for element and click
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            
            # Wait for URL change
            self.wait.until(EC.url_contains(expected_url))
            self.logger.info(f"Successfully navigated to {section}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to {section}: {str(e)}")
            return False

    def verify_logo_visible(self):
        """Verify that the sidebar logo is visible"""
        self.wait_for_sidebar_load()
        return self.is_element_visible(self.HEADER_LOGO)

    def click_close_button(self):
        """Click the close button on the sidebar"""
        self.wait_for_sidebar_load()
        try:
            button = self.wait.until(EC.element_to_be_clickable(self.CLOSE_BUTTON))
            self.driver.execute_script("arguments[0].click();", button)
            # Wait for sidebar to close (you may need to adjust this based on actual behavior)
            self.wait.until_not(EC.visibility_of_element_located(self.HEADER_LOGO))
            return True
        except Exception as e:
            self.logger.error(f"Failed to click close button: {str(e)}")
            return False

    def navigate_to_system_settings_item(self, item):
        """Navigate to a specific System Settings submenu item"""
        try:
            # First ensure menu is expanded
            if not self.expand_system_settings():
                return False

            # Map items to locators and URLs
            item_mapping = {
                'categories': (self.CATEGORIES_LINK, '/admin/categories'),
                'areas': (self.AREAS_LINK, '/admin/areas'),
                'announcement_categories': (self.ANNOUNCEMENT_CATEGORIES_LINK, '/admin/announcement-categories')
            }
            
            if item not in item_mapping:
                raise ValueError(f"Unknown system settings item: {item}")
            
            locator, expected_url = item_mapping[item]
            
            # Wait for item to be visible and clickable
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            
            # Use JavaScript click for reliability
            self.driver.execute_script("arguments[0].click();", element)
            
            # Wait for navigation
            self.wait.until(
                EC.url_contains(expected_url)
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to {item}: {str(e)}")
            return False

    def navigate_to_inquiries_item(self, item):
        """Navigate to a specific Inquiries submenu item"""
        try:
            # First ensure menu is expanded
            if not self.expand_inquiries():
                return False

            # Map items to locators and URLs
            item_mapping = {
                'messages': (self.MESSAGES_LINK, '/admin/messages'),
                'function_room': (self.FUNCTION_ROOM_LINK, '/admin/function-room-inquiries')
            }
            
            if item not in item_mapping:
                raise ValueError(f"Unknown inquiries item: {item}")
            
            locator, expected_url = item_mapping[item]
            
            # Wait for item to be visible and clickable
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            
            # Use JavaScript click for reliability
            self.driver.execute_script("arguments[0].click();", element)
            
            # Wait for navigation
            self.wait.until(
                EC.url_contains(expected_url)
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to {item}: {str(e)}")
            return False
