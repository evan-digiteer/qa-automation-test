import pytest
from pages.login_page import LoginPage

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        self.driver.get(self.config.base_url)

    def test_successful_login(self):
        """Test successful login with valid credentials"""
        self.login_page.login(self.config.username, self.config.password)
        # Add assertion for successful login - depends on your application's behavior
        assert self.driver.current_url != self.config.base_url, "Login failed - URL didn't change"

    def test_empty_credentials(self):
        """Test login attempt with empty credentials"""
        self.login_page.login("", "")
        assert self.login_page.is_error_message_displayed(), "Error message not displayed for empty credentials"

    def test_empty_email(self):
        """Test login attempt with empty email"""
        self.login_page.login("", self.config.password)
        assert self.login_page.is_error_message_displayed(), "Error message not displayed for empty email"

    def test_empty_password(self):
        """Test login attempt with empty password"""
        self.login_page.login(self.config.username, "")
        assert self.login_page.is_error_message_displayed(), "Error message not displayed for empty password"

    def test_invalid_email_format(self):
        """Test login attempt with invalid email format"""
        self.login_page.login("invalid_email", self.config.password)
        assert self.login_page.is_error_message_displayed(), "Error message not displayed for invalid email format"

    def test_invalid_credentials(self):
        """Test login attempt with invalid credentials"""
        self.login_page.login("invalid@email.com", "wrong_password")
        assert self.login_page.is_error_message_displayed(), "Error message not displayed for invalid credentials"

    @pytest.mark.parametrize("email,password", [
        ("test@email.com", "short"),  # Password too short
        ("test@email.com", "a" * 100),  # Password too long
        ("a" * 100 + "@email.com", "valid_password"),  # Email too long
        ("<script>alert(1)</script>", "valid_password"),  # XSS attempt
        ("' OR '1'='1", "' OR '1'='1"),  # SQL injection attempt
    ])
    def test_invalid_input_variations(self, email, password):
        """Test login attempts with various invalid inputs"""
        self.login_page.login(email, password)
        assert self.login_page.is_error_message_displayed(), f"Error message not displayed for invalid input: {email}, {password}"

    def test_field_group_visibility(self):
        """Test if login form fields are visible"""
        assert self.login_page.is_field_group_displayed(), "Login form fields not displayed"

    @pytest.mark.xfail(reason="This test should fail to demonstrate screenshot capture")
    def test_failed_scenario_for_screenshot(self):
        """Intentionally failing test to demonstrate screenshot capture"""
        self.login_page.login(self.config.username, self.config.password)
        assert False, "Intentional failure to demonstrate screenshot capture"
