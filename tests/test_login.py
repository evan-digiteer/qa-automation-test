import pytest
from pages.login_page import LoginPage
from data.constants import ValidationData, URLs, ExpectedElements

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        # Use URLs constant
        full_url = self.config.base_url + URLs.LOGIN_PAGE
        self.login_page.logger.info(f"Navigating to login page: {full_url}")
        self.driver.get(full_url)

    def test_successful_login(self):
        """Test successful login with valid credentials"""
        self.login_page.login(self.config.username, self.config.password)
        # Use URLs constant for dashboard
        expected_url = self.config.base_url + URLs.DASHBOARD
        self.login_page.logger.info(f"Current URL: {self.driver.current_url}")
        self.login_page.logger.info(f"Expected URL: {expected_url}")
        assert expected_url in self.driver.current_url, "Login did not redirect to dashboard"

    def test_empty_credentials(self):
        """Test login attempt with empty credentials"""
        self.login_page.login("", "")
        assert self.login_page.is_error_message_displayed(), "Error message not displayed for empty credentials"

    def test_invalid_credentials(self):
        """Test login attempt with invalid credentials"""
        self.login_page.login("wrong@email.com", "wrongpassword")
        assert self.login_page.is_error_message_displayed(), "Error message not displayed for invalid credentials"

    def test_field_visibility(self):
        """Test if login form fields are visible"""
        assert self.login_page.is_field_group_displayed(), "Login form fields not displayed"

