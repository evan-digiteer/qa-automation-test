from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC  # Add this import
from selenium.webdriver.support.ui import WebDriverWait  # Add this import
from faker import Faker
from .base_page import BasePage
from data.constants import AddUserPage as Constants

class AddUserPage(BasePage):
    # Form Elements
    USER_FORM = (By.ID, "new_user")
    FORM_ERROR_STREAM = (By.ID, "formErrorStream")
    
    # Header Elements
    TITLE = (By.CSS_SELECTOR, ".card__header .fw-bold")
    BACK_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Back']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.btn.btn--success")
    DISCARD_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--outline-danger[href='/admin/users']")
    
    # Photo Elements
    USER_PHOTO_PREVIEW = (By.ID, "userPhotoPreview")
    UPLOAD_PHOTO_INPUT = (By.ID, "member-photo")
    UPLOAD_PHOTO_BUTTON = (By.CSS_SELECTOR, ".btn.btn--primary.btn--block.upload-btn")
    REMOVE_PHOTO_BUTTON = (By.CSS_SELECTOR, ".btn.btn--outline-primary.btn--block")
    REMOVE_PHOTO_HIDDEN = (By.ID, "remove-photo")
    
    # Input Fields
    FIRST_NAME_INPUT = (By.ID, "user_first_name")
    MIDDLE_NAME_INPUT = (By.ID, "user_middle_name")
    LAST_NAME_INPUT = (By.ID, "user_last_name")
    EMAIL_INPUT = (By.ID, "user_email")
    
    # Role Selection
    ROLE_SELECT = (By.ID, "division-id")
    ROLE_DROPDOWN = (By.CSS_SELECTOR, ".ts-wrapper.single")
    ROLE_INPUT = (By.CSS_SELECTOR, ".ts-control")
    ROLE_OPTIONS = (By.CSS_SELECTOR, ".ts-dropdown-content")
    
    # Field Groups
    FIELD_GROUP = (By.CLASS_NAME, "field-group")
    FIELD_CONTAINER = (By.CLASS_NAME, "field-container")
    FIELD_HELPER = (By.CLASS_NAME, "field-helper")
    REQUIRED_LABEL = (By.CLASS_NAME, "label--required")

    # Alert Messages
    ALERT_MESSAGE = (By.CSS_SELECTOR, ".alert--soft-danger ul li")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def fill_user_form(self, user_data=None):
        """Fill user form with provided data or generate fake data"""
        if user_data is None:
            user_data = {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name(),
                'email': self.faker.email(),
                'role': 'Administrator'
                # Removed is_active since there's no toggle
            }
        
        self.type(self.FIRST_NAME_INPUT, user_data['first_name'])
        self.type(self.LAST_NAME_INPUT, user_data['last_name'])
        self.type(self.EMAIL_INPUT, user_data['email'])
        
        # Handle role selection
        role_select = Select(self.find_element(self.ROLE_SELECT))
        role_select.select_by_visible_text(user_data['role'])
        
        return user_data

    def save_user(self):
        """Click save button and wait for redirect"""
        try:
            self.logger.info("Saving new user")
            current_url = self.driver.current_url
            
            # Click save button
            self.click(self.SAVE_BUTTON)
            
            # Wait for URL to change with longer timeout
            long_wait = WebDriverWait(self.driver, 30)  # Increased timeout
            long_wait.until(EC.url_contains('/admin/users'))
            long_wait.until(lambda d: d.current_url != current_url)
            
            # Wait for page load and table
            long_wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table')))
            long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr')))
            
            # Extra wait for data to settle
            self.driver.implicitly_wait(3)
            
            self.logger.info("User saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save user: {str(e)}")
            return False

    def discard_changes(self):
        """Click discard button and wait for navigation back to users page"""
        try:
            self.logger.info("Discarding changes and returning to users page")
            current_url = self.driver.current_url
            
            # Click discard button
            self.click(self.DISCARD_BUTTON)
            
            # Wait for URL to change to users page
            self.wait.until(EC.url_contains('/admin/users'))
            self.wait.until(lambda d: d.current_url != current_url)
            
            # Wait for users table to be visible
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table')))
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to discard changes: {str(e)}")
            return False

    def create_user(self, user_data=None):
        """Complete flow to create a new user"""
        filled_data = self.fill_user_form(user_data)
        self.save_user()
        return filled_data

    def get_inline_error(self):
        """Get the text of inline error message if present"""
        return self.get_text(self.INLINE_ERROR)

    def is_error_message_displayed(self, expected_message=None):
        """Check for error message in alert or inline validation"""
        try:
            # Check for alert message first
            try:
                alert = self.find_element(self.ALERT_MESSAGE)
                if alert.is_displayed():
                    error_text = alert.text.strip()
                    self.logger.info(f"Found alert message: {error_text}")
                    if expected_message:
                        return error_text == expected_message
                    return True
            except:
                # If no alert, check inline errors
                self.logger.info("No alert message found, checking inline errors")
                for field_group in self.find_elements(self.FIELD_GROUP):
                    try:
                        inline_error = field_group.find_element(*self.INLINE_ERROR)
                        if inline_error.is_displayed():
                            error_text = inline_error.text.strip()
                            self.logger.info(f"Found inline error: {error_text}")
                            if expected_message:
                                return error_text == expected_message
                            return True
                    except:
                        continue
                
            self.logger.info("No error messages found")
            return False
        except Exception as e:
            self.logger.error(f"Error checking for messages: {str(e)}")
            return False
