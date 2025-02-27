import pytest
import logging
from pages.login_page import LoginPage
from data.constants import LoginPage as Constants

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Navigate to login page
        self.driver.get(f"{self.config.base_url}{Constants.URLS['LOGIN']}")

    def test_login_page_elements(self):
        """Verify all elements are present on login page"""
        elements_to_check = {
            "Heading": {
                "locator": self.login_page.LOGIN_HEADING,
                "expected": Constants.HEADING
            },
            "Email Field": {
                "locator": self.login_page.EMAIL_FIELD,
                "expected": Constants.PLACEHOLDERS["EMAIL"]
            },
            "Password Field": {
                "locator": self.login_page.PASSWORD_FIELD,
                "expected": Constants.PLACEHOLDERS["PASSWORD"]
            }
        }
        
        self.logger.info("Verifying page elements:")
        verification_results = []
        
        for name, data in elements_to_check.items():
            element = self.login_page.find_element(data["locator"])
            actual = element.text if name == "Heading" else element.get_attribute("placeholder")
            is_displayed = element.is_displayed()
            
            result = {
                "element": name,
                "visible": is_displayed,
                "expected": data["expected"],
                "actual": actual,
                "passed": is_displayed and actual == data["expected"]
            }
            verification_results.append(result)
            
            self.logger.info(f"\n{name}:")
            self.logger.info(f"  Visible: {is_displayed}")
            self.logger.info(f"  Expected: {data['expected']}")
            self.logger.info(f"  Actual: {actual}")
            
        # Assert all verifications passed
        failed = [r for r in verification_results if not r["passed"]]
        if failed:
            failure_details = "\n".join(
                f"{r['element']}:\n  Visible: {r['visible']}\n  Expected: {r['expected']}\n  Actual: {r['actual']}"
                for r in failed
            )
            assert False, f"Page element verification failed:\n{failure_details}"

    def test_successful_login(self):
        """Test successful login with valid credentials"""
        expected_url = f"{self.config.base_url}/admin/dashboard"
        self.logger.info(f"Attempting login with: {self.config.username}")
        self.logger.info(f"Expected redirect: {expected_url}")
        
        # Perform login
        login_success = self.login_page.login(self.config.username, self.config.password)
        actual_url = self.driver.current_url
        
        self.logger.info(f"Login success: {login_success}")
        self.logger.info(f"Actual URL: {actual_url}")
        
        assert login_success, "Login attempt failed"
        assert Constants.URLS["DASHBOARD"] in actual_url, \
            f"Redirect failed\nExpected URL to contain: {Constants.URLS['DASHBOARD']}\nActual URL: {actual_url}"

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        invalid_credentials = {
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
        
        expected_message = Constants.MESSAGES["INVALID_CREDENTIALS"]
        self.logger.info(f"Testing invalid login with email: {invalid_credentials['email']}")
        self.logger.info(f"Expected error message: {expected_message}")
        
        # Attempt login
        self.login_page.login(invalid_credentials["email"], invalid_credentials["password"])
        
        # Verify error message
        error_alert = self.login_page.find_element(self.login_page.ERROR_ALERT)
        actual_message = error_alert.text.strip()
        
        self.logger.info(f"Actual error message: {actual_message}")
        
        assert error_alert.is_displayed(), "Error alert not displayed"
        assert actual_message == expected_message, \
            f"Error message mismatch\nExpected: {expected_message}\nActual: {actual_message}"

    def test_empty_fields_validation(self):
        """Test validation for empty fields"""
        expected_message = Constants.MESSAGES["REQUIRED_FIELD"]
        self.logger.info(f"Testing empty fields validation")
        self.logger.info(f"Expected message: {expected_message}")
        
        # Click login without entering credentials
        self.login_page.click(self.login_page.LOGIN_BUTTON)
        
        # Get all error messages
        fields = self.login_page.find_elements(self.login_page.FIELD_HELPER)
        error_texts = [field.text.strip() for field in fields if field.is_displayed()]
        
        self.logger.info(f"Found error messages: {error_texts}")
        
        assert expected_message in error_texts, \
            f"Required field message not found\nExpected: {expected_message}\nFound messages: {error_texts}"

    def test_credentials_loaded(self, config):
        """Verify credentials are loaded from environment"""
        assert config.username, "Username not loaded from environment"
        assert config.password, "Password not loaded from environment"
        self.logger.info(f"Credentials loaded - Username: {config.username[:3]}***")

    def test_password_visibility_toggle(self):
        """Test password field show/hide functionality"""
        self.logger.info("Testing password visibility toggle")
        
        # Get password field and toggle button
        password_field = self.login_page.find_element(self.login_page.PASSWORD_FIELD)
        toggle_button = self.login_page.find_element(self.login_page.SHOW_PASSWORD_BUTTON)
        
        # Initial state check
        initial_type = password_field.get_attribute("type")
        self.logger.info(f"Initial password field type: {initial_type}")
        assert initial_type == Constants.ATTRIBUTES["PASSWORD_HIDDEN"], \
            f"Password should be hidden initially\nExpected: {Constants.ATTRIBUTES['PASSWORD_HIDDEN']}\nActual: {initial_type}"
        
        # Click show password button
        self.logger.info("Clicking show password button")
        toggle_button.click()
        
        # Verify password is visible
        shown_type = password_field.get_attribute("type")
        self.logger.info(f"Password field type after show: {shown_type}")
        assert shown_type == Constants.ATTRIBUTES["PASSWORD_VISIBLE"], \
            f"Password should be visible after clicking show\nExpected: {Constants.ATTRIBUTES['PASSWORD_VISIBLE']}\nActual: {shown_type}"
        
        # Click hide password button
        self.logger.info("Clicking hide password button")
        toggle_button.click()
        
        # Verify password is hidden again
        hidden_type = password_field.get_attribute("type")
        self.logger.info(f"Password field type after hide: {hidden_type}")
        assert hidden_type == Constants.ATTRIBUTES["PASSWORD_HIDDEN"], \
            f"Password should be hidden after clicking hide\nExpected: {Constants.ATTRIBUTES['PASSWORD_HIDDEN']}\nActual: {hidden_type}"

