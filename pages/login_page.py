from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from data.constants import ValidationData, ExpectedElements

class LoginPage(BasePage):
    # Login Form Elements
    EMAIL_INPUT = (By.ID, "user_email")
    PASSWORD_INPUT = (By.ID, "user_password")
    LOGIN_BUTTON = (By.XPATH, '//button[contains(@class, "btn--primary") and contains(@class, "btn--lg")]')
    
    # Update Logout Elements
    PROFILE_DROPDOWN = (By.XPATH, '//button[contains(@class, "header__dropdown-btn") and @data-bs-toggle="dropdown"]')
    LOGOUT_BUTTON = (By.XPATH, '//button[@class="dropdown-menu__link" and contains(text(), "Log Out")]')
    
    # Validation Elements
    FIELD_GROUP = (By.CLASS_NAME, 'field-group')
    INLINE_ERROR = (By.CLASS_NAME, 'field-helper')
    
    # Error Messages
    REQUIRED_FIELD_ERROR = ValidationData.ERROR_MESSAGES["REQUIRED_FIELD"]

    # Basic Actions
    def login(self, username, password):
        """Perform login with given credentials"""
        self.type(self.EMAIL_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def logout(self):
        """Perform logout action with proper waits"""
        try:
            self.logger.info("Attempting to logout")
            # Wait for page to be fully loaded before attempting logout
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            # Wait for dropdown to be clickable and click it
            self.wait.until(EC.element_to_be_clickable(self.PROFILE_DROPDOWN))
            self.click(self.PROFILE_DROPDOWN)
            
            # Wait for logout button to be clickable and click it
            self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON))
            self.click(self.LOGOUT_BUTTON)
            
            # Wait for redirect to login page
            self.wait.until(EC.url_contains("login"))
            return True
        except Exception as e:
            self.logger.error(f"Error during logout: {str(e)}")
            return False

    # Error Handling and Validation
    def get_inline_error(self):
        """Get the text of inline error message if present"""
        return self.get_text(self.INLINE_ERROR)

    def is_error_message_displayed(self):
        """Check if any error message is displayed for username or password"""
        try:
            self.logger.info("Checking for error messages on the login form")
            field_groups = self.find_elements(self.FIELD_GROUP)
            
            for field_group in field_groups:
                try:
                    inline_error = field_group.find_element(*self.INLINE_ERROR)
                    if inline_error.is_displayed() and inline_error.text.strip() == self.REQUIRED_FIELD_ERROR:
                        self.logger.warning(f"Error message displayed: {inline_error.text}")
                        return True
                except:
                    continue
            
            self.logger.info("No error message displayed")
            return False
        except Exception as e:
            self.logger.error(f"Error checking for error message: {str(e)}")
            return False

    # Page Verification
    def verify_page_elements(self):
        """Verify all expected elements are present with correct text"""
        expected = ExpectedElements.LOGIN_PAGE
        try:
            assert self.driver.title == expected["title"], "Page title is incorrect"
            assert self.find_element(self.EMAIL_INPUT).get_attribute("placeholder") == expected["email_placeholder"]
            assert self.find_element(self.PASSWORD_INPUT).get_attribute("placeholder") == expected["password_placeholder"]
            assert self.find_element(self.LOGIN_BUTTON).text == expected["login_button_text"]
            return True
        except AssertionError as e:
            self.logger.error(f"Page element verification failed: {str(e)}")
            return False
