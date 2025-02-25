import pytest
from pages.login_page import LoginPage
from data.constants import ValidationData, URLs, ExpectedElements
from selenium.webdriver.support.ui import WebDriverWait

class TestLogin:
    # Test Setup
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        # Navigate to login page using URLs constant
        login_url = self.config.base_url + URLs.LOGIN_PAGE
        self.login_page.logger.info(f"Navigating to login page: {login_url}")
        self.driver.get(login_url)

    def test_successful_login(self):
        """Test successful login with valid credentials"""
        self.login_page.login(self.config.username, self.config.password)
        expected_url = self.config.base_url + URLs.DASHBOARD
        self.login_page.logger.info(f"Current URL: {self.driver.current_url}")
        self.login_page.logger.info(f"Expected URL: {expected_url}")
        assert expected_url in self.driver.current_url, "Login did not redirect to dashboard"

    def test_empty_credentials(self):
        """Test login attempt with empty credentials"""
        self.login_page.login("", "")
        assert self.login_page.is_error_message_displayed(), \
            f"Expected error message: {ValidationData.ERROR_MESSAGES['REQUIRED_FIELD']}"

    def test_invalid_credentials(self):
        """Test login attempt with invalid credentials"""
        self.login_page.login("wrong@email.com", "wrongpassword")
        assert self.login_page.is_error_message_displayed(), \
            f"Expected error message: {ValidationData.ERROR_MESSAGES['INVALID_CREDENTIALS']}"

    def test_login_form_visibility(self):
        """Verify login form elements are visible and match expected content"""
        assert self.login_page.verify_page_elements(), \
            "Login page elements do not match expected content"

    def test_browser_back_after_logout(self):
        """Test that browser back button after logout doesn't allow access to protected pages"""
        # Login first
        self.login_page.login(self.config.username, self.config.password)
        dashboard_url = self.config.base_url + URLs.DASHBOARD
        assert dashboard_url in self.driver.current_url, "Login failed"

        # Wait for page load before logout
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        # Perform logout and wait for completion
        self.login_page.logout()
        assert URLs.LOGIN_PAGE in self.driver.current_url, "Logout failed"

        # Wait before trying browser back
        self.driver.implicitly_wait(2)  # Short wait before back navigation
        self.driver.back()
        self.login_page.logger.info("Attempted to navigate back after logout")
        
        # Wait for any redirects to complete
        WebDriverWait(self.driver, 10).until(
            lambda driver: URLs.LOGIN_PAGE in driver.current_url
        )
        
        assert URLs.LOGIN_PAGE in self.driver.current_url, "Browser back after logout allowed access to protected page"

