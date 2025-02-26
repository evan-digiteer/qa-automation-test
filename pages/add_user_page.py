from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from faker import Faker
from .base_page import BasePage
from data.constants import ValidationData

class AddUserPage(BasePage):
    # Form Fields
    FIRST_NAME_INPUT = (By.ID, "first_name")
    LAST_NAME_INPUT = (By.ID, "last_name")
    EMAIL_INPUT = (By.ID, "email")
    ROLE_SELECT = (By.ID, "roleid")
    STATUS_TOGGLE = (By.ID, "user_active")
    
    # Buttons
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.btn--primary[type='submit']")
    DISCARD_BUTTON = (By.CSS_SELECTOR, "a.btn--default[href='/admin/users']")
    
    # Validation Elements (same as LoginPage)
    FIELD_GROUP = (By.CLASS_NAME, 'field-group')
    INLINE_ERROR = (By.CLASS_NAME, 'field-helper')
    REQUIRED_FIELD_ERROR = ValidationData.ERROR_MESSAGES["REQUIRED_FIELD"]
    
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
                'role': 'Administrator',
                'is_active': True
            }
        
        self.type(self.FIRST_NAME_INPUT, user_data['first_name'])
        self.type(self.LAST_NAME_INPUT, user_data['last_name'])
        self.type(self.EMAIL_INPUT, user_data['email'])
        
        # Handle role selection
        role_select = Select(self.find_element(self.ROLE_SELECT))
        role_select.select_by_visible_text(user_data['role'])
        
        # Handle status toggle
        status_checkbox = self.find_element(self.STATUS_TOGGLE)
        if status_checkbox.is_selected() != user_data['is_active']:
            status_checkbox.click()
        
        return user_data

    def save_user(self):
        """Click save button and return success status"""
        self.logger.info("Saving new user")
        self.click(self.SAVE_BUTTON)
        return True

    def discard_changes(self):
        """Click discard button to cancel user creation"""
        self.logger.info("Discarding changes")
        self.click(self.DISCARD_BUTTON)
        return True

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
