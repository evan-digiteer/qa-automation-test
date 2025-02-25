from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from data.constants import ValidationData, ExpectedElements

class LoginPage(BasePage):
    # Login Form Elements
    EMAIL_INPUT = (By.ID, "user_email")
    PASSWORD_INPUT = (By.ID, "user_password")
    LOGIN_BUTTON = (By.XPATH, '//button[contains(@class, "btn--primary") and contains(@class, "btn--lg")]')
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(@href, '/admin/forgot/new')]")
    
    # Update Logout Elements
    PROFILE_DROPDOWN = (By.XPATH, '//button[contains(@class, "header__dropdown-btn") and @data-bs-toggle="dropdown"]')
    LOGOUT_BUTTON = (By.XPATH, '//button[@class="dropdown-menu__link" and contains(text(), "Log Out")]')
    
    # Validation Elements
    FIELD_GROUP = (By.CLASS_NAME, 'field-group')
    INLINE_ERROR = (By.CLASS_NAME, 'field-helper')
    
    # Error Messages
    REQUIRED_FIELD_ERROR = ValidationData.ERROR_MESSAGES["REQUIRED_FIELD"]

    # Add new element locators
    EMAIL_LABEL = (By.XPATH, "//label[@for='user_email']")
    PASSWORD_LABEL = (By.XPATH, "//label[@for='user_password']")
    LOGIN_CONTAINER = (By.CLASS_NAME, "login-container")
    LOGIN_FORM = (By.TAG_NAME, "form")

    # Update locators to match HTML structure
    CARD_CONTENT = (By.CLASS_NAME, "card__content")
    LOGIN_FORM = (By.CLASS_NAME, "new_user")
    LOGO_IMAGE = (By.CSS_SELECTOR, "img[alt='alt']")
    LOGIN_HEADING = (By.CSS_SELECTOR, "h6")
    EMAIL_LABEL = (By.XPATH, "//label[contains(@class, 'label--required') and text()='Email']")
    PASSWORD_LABEL = (By.XPATH, "//label[contains(@class, 'label--required') and text()='Password']")
    SHOW_PASSWORD_BUTTON = (By.CSS_SELECTOR, "button[data-controller='admin--show-password']")

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
        """Verify essential elements are present and correct"""
        expected = ExpectedElements.LOGIN_PAGE
        errors = []
        
        try:
            # Check title
            actual_title = self.driver.title
            self.logger.info(f"Checking page title - Expected: '{expected['title']}', Found: '{actual_title}'")
            if actual_title != expected["title"]:
                errors.append(f"Title mismatch - Expected: '{expected['title']}', Found: '{actual_title}'")

            # Check email field
            try:
                email_field = self.find_element(self.EMAIL_INPUT)
                if not email_field.is_displayed():
                    errors.append("Email field is not visible")
                else:
                    actual_email_placeholder = email_field.get_attribute("placeholder") or ""
                    self.logger.info(f"Email field visible: True, placeholder: '{actual_email_placeholder}'")
                    if not actual_email_placeholder:
                        errors.append("Email placeholder is missing")
                    elif actual_email_placeholder != expected["email_placeholder"]:
                        errors.append(f"Email placeholder mismatch - Expected: '{expected['email_placeholder']}', Found: '{actual_email_placeholder}'")
            except Exception as e:
                errors.append(f"Error checking email field: {str(e)}")

            # Check password field
            try:
                password_field = self.find_element(self.PASSWORD_INPUT)
                if not password_field.is_displayed():
                    errors.append("Password field is not visible")
                else:
                    actual_password_placeholder = password_field.get_attribute("placeholder") or ""
                    self.logger.info(f"Password field visible: True, placeholder: '{actual_password_placeholder}'")
                    if not actual_password_placeholder:
                        errors.append("Password placeholder is missing")
                    elif actual_password_placeholder != expected["password_placeholder"]:
                        errors.append(f"Password placeholder mismatch - Expected: '{expected['password_placeholder']}', Found: '{actual_password_placeholder}'")
            except Exception as e:
                errors.append(f"Error checking password field: {str(e)}")

            # Check login button
            try:
                login_button = self.find_element(self.LOGIN_BUTTON)
                if not login_button.is_displayed():
                    errors.append("Login button is not visible")
                else:
                    actual_button_text = login_button.text
                    self.logger.info(f"Login button visible: True, text: '{actual_button_text}'")
                    if actual_button_text != expected["login_button_text"]:
                        errors.append(f"Login button text mismatch - Expected: '{expected['login_button_text']}', Found: '{actual_button_text}'")
            except Exception as e:
                errors.append(f"Error checking login button: {str(e)}")

            # Check forgot password link
            try:
                forgot_link = self.find_element(self.FORGOT_PASSWORD_LINK)
                if not forgot_link.is_displayed():
                    errors.append("Forgot password link is not visible")
                else:
                    self.logger.info("Forgot password link is visible")
            except Exception as e:
                errors.append(f"Error checking forgot password link: {str(e)}")

            # Report results
            if errors:
                for error in errors:
                    self.logger.error(error)
                return False
            
            self.logger.info("All essential page elements verified successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Unexpected error during page element verification: {str(e)}")
            return False
