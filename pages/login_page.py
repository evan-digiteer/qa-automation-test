from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Class level locators using UPPERCASE for constants
    EMAIL_INPUT = (By.ID, "user_email")
    PASSWORD_INPUT = (By.ID, "user_password")
    LOGIN_BUTTON = (By.XPATH, '//button[contains(@class, "btn--primary") and contains(@class, "btn--lg")]')
    FIELD_GROUP = (By.CLASS_NAME, 'field-group')
    INLINE_ERROR = (By.CLASS_NAME, 'field-helper')

    REQUIRED_FIELD_ERROR = "This field is required"

    def login(self, username, password):
        self.type(self.EMAIL_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_inline_error(self):
        return self.get_text(self.INLINE_ERROR)

    def is_field_group_displayed(self):
        return self.find_element(self.FIELD_GROUP).is_displayed()

    def is_error_message_displayed(self):
        """Check if any error message is displayed for username or password."""
        try:
            self.logger.info("Checking for error messages on the login form.")
            field_groups = self.find_elements(self.FIELD_GROUP)
            
            for field_group in field_groups:
                try:
                    inline_error = field_group.find_element(*self.INLINE_ERROR)
                    if inline_error.is_displayed() and inline_error.text.strip() == self.REQUIRED_FIELD_ERROR:
                        self.logger.warning(f"Error message displayed: {inline_error.text}")
                        return True
                except:
                    continue

            self.logger.info("No error message displayed.")
            return False

        except Exception as e:
            self.logger.error(f"Error occurred while checking for error message: {str(e)}")
            return False

    def get_field_error(self, field_group):
        """Get error message for a specific field group"""
        try:
            return field_group.find_element(*self.INLINE_ERROR).text.strip()
        except:
            return None
