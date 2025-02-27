from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from data.constants import LoginPage as Constants

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # Form Element
    LOGIN_FORM = (By.ID, "new_user")
    
    # Input Fields
    EMAIL_FIELD = (By.ID, "user_email")
    PASSWORD_FIELD = (By.ID, "user_password")
    
    # Buttons
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.btn.btn--primary.btn--block.btn--lg")
    SHOW_PASSWORD_BUTTON = (By.CSS_SELECTOR, "button[data-controller='admin--show-password']")
    
    # Labels and Text Elements
    LOGIN_HEADING = (By.CSS_SELECTOR, "h6")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label.label.label--required")
    LOGO_IMAGE = (By.CSS_SELECTOR, "img.mb-4[alt='alt']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href='/admin/forgot/new']")
    
    # Field Groups
    EMAIL_FIELD_GROUP = (By.CSS_SELECTOR, ".field-group:nth-child(2)")
    PASSWORD_FIELD_GROUP = (By.CSS_SELECTOR, ".field-group:nth-child(3)")
    
    # Input Containers
    EMAIL_CONTAINER = (By.CSS_SELECTOR, ".field-container")
    PASSWORD_CONTAINER = (By.CSS_SELECTOR, ".field-container")
    
    # Error Elements
    FIELD_HELPER = (By.CLASS_NAME, "field-helper")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert.alert--danger")

    def login(self, email, password):
        """Perform login with given credentials"""
        try:
            self.logger.info(f"Attempting to login with email: {email}")
            
            # Wait for form to be ready
            self.wait.until(EC.presence_of_element_located(self.LOGIN_FORM))
            self.wait.until(EC.element_to_be_clickable(self.EMAIL_FIELD))
            
            # Clear and type credentials
            self.find_element(self.EMAIL_FIELD).clear()
            self.type(self.EMAIL_FIELD, email)
            self.logger.info("Email entered")
            
            self.find_element(self.PASSWORD_FIELD).clear()
            self.type(self.PASSWORD_FIELD, password)
            self.logger.info("Password entered")
            
            # Wait for and click login button
            login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
            login_button.click()
            self.logger.info("Login button clicked")
            
            # Wait for either success or error
            self.wait.until(lambda d: 
                "/admin/dashboard" in d.current_url or
                self.is_element_visible(self.ERROR_ALERT)
            )
            
            if "/admin/dashboard" in self.driver.current_url:
                self.logger.info("Login successful")
                return True
            else:
                self.logger.warning("Login failed - error alert displayed")
                return False
                
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return False

    def toggle_password_visibility(self):
        """Toggle password field visibility"""
        try:
            self.logger.info("Toggling password visibility")
            show_button = self.find_element(self.SHOW_PASSWORD_BUTTON)
            self.click(self.SHOW_PASSWORD_BUTTON)
            
            # Get password field type after toggle
            password_field = self.find_element(self.PASSWORD_INPUT)
            return password_field.get_attribute("type")
        except Exception as e:
            self.logger.error(f"Error toggling password visibility: {str(e)}")
            return None

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

    def get_inline_error(self):
        """Get the text of inline error message if present"""
        return self.get_text(self.INLINE_ERROR)

    def is_error_message_displayed(self):
        """Check if any error message is displayed (inline or alert)"""
        try:
            self.logger.info("Checking for error messages on the login form")
            
            # Check for alert error
            try:
                error_alert = self.find_element(self.ERROR_ALERT)
                if error_alert.is_displayed():
                    actual_text = error_alert.text.strip().lower().replace('.', '')
                    expected_text = ValidationData.ERROR_MESSAGES["INVALID_CREDENTIALS"].lower().replace('.', '')
                    if actual_text == expected_text:
                        self.logger.warning(f"Alert error displayed: {error_alert.text}")
                        return True
            except:
                pass
            
            # Check for inline errors
            field_groups = self.find_elements(self.FIELD_GROUP)
            for field_group in field_groups:
                try:
                    inline_error = field_group.find_element(*self.INLINE_ERROR)
                    if inline_error.is_displayed() and inline_error.text.strip() == self.REQUIRED_FIELD_ERROR:
                        self.logger.warning(f"Inline error displayed: {inline_error.text}")
                        return True
                except:
                    continue
            
            self.logger.info("No error message displayed")
            return False
        except Exception as e:
            self.logger.error(f"Error checking for error message: {str(e)}")
            return False

    def verify_page_elements(self):
        """Verify essential elements are present and correct"""
        try:
            # Wait for form elements to be present
            self.wait.until(EC.presence_of_element_located(self.LOGIN_FORM))
            
            # Check page heading instead of title
            heading = self.find_element(self.LOGIN_HEADING)
            if heading.text != Constants.HEADING:
                self.logger.error(f"Heading mismatch - Expected: '{Constants.HEADING}', Found: '{heading.text}'")
                return False

            # Check fields and verify they're usable
            for field_id, placeholder in [
                (self.EMAIL_FIELD, Constants.PLACEHOLDERS["EMAIL"]),
                (self.PASSWORD_FIELD, Constants.PLACEHOLDERS["PASSWORD"])
            ]:
                field = self.wait.until(EC.element_to_be_clickable(field_id))
                if not field.is_displayed():
                    self.logger.error(f"Field not visible: {field_id}")
                    return False
                if field.get_attribute("placeholder") != placeholder:
                    self.logger.error(f"Placeholder mismatch for {field_id}")
                    return False

            # Check login button is clickable
            if not self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)):
                self.logger.error("Login button not clickable")
                return False

            self.logger.info("All essential page elements verified successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during page verification: {str(e)}")
            return False
