import pytest
import logging
from pages.add_user_page import AddUserPage
from pages.users_page import UsersPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from data.constants import LoginPage as LoginConstants
from data.constants import AddUserPage as Constants
from faker import Faker

class TestAddUser:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.faker = Faker()
        self.add_user_page = AddUserPage(driver)
        self.users_page = UsersPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        
        # Login first using LoginPage
        self.logger.info("Logging in before add user tests")
        self.driver.get(f"{config.base_url}{LoginConstants.URLS['LOGIN']}")
        assert self.login_page.login(config.username, config.password), "Login failed"
        
        # Navigate to users page using side menu
        self.logger.info("Navigating to Users page")
        assert self.side_menu.navigate_to_users(), "Failed to navigate to Users page"
        
        # Wait for users page and click add user
        assert self.users_page.wait_for_users_table(), "Users table failed to load"
        self.users_page.click(self.users_page.NEW_USER_BUTTON)
        self.logger.info("Setup completed successfully")

    def test_create_user_with_valid_data(self):
        """Test creating a new user with valid data"""
        # Create user with generated data
        user_data = self.add_user_page.create_user()
        
        # Wait for navigation and table update
        self.users_page.wait_for_users_table()
        
        # Search for the user to verify
        self.users_page.search_user(user_data['email'], search_type="email")
        
        # Verify user appears in search results
        assert self.users_page.is_user_present(user_data['email']), \
            f"New user {user_data['email']} not found in users table"

    def test_discard_user_creation(self):
        """Test discarding user creation"""
        # Fill form but don't save
        user_data = self.add_user_page.fill_user_form()
        self.add_user_page.discard_changes()
        
        # Verify back on users page by checking URL and table presence
        assert '/admin/users' in self.driver.current_url, "Not returned to users page"
        assert self.users_page.wait_for_users_table(), "Users table not loaded"
        
        # Verify user not created
        assert not self.users_page.is_user_present(user_data['email']), \
            f"User {user_data['email']} should not exist after discard"
        
        self.logger.info("Successfully discarded user creation")

    def test_required_fields_validation(self):
        """Test required fields validation"""
        self.add_user_page.click(self.add_user_page.SAVE_BUTTON)
        assert self.add_user_page.is_error_message_displayed(), \
            "Required field validation message not displayed"

    def test_duplicate_email_validation(self):
        """Test that duplicate email addresses are not allowed"""
        # Create first user with generated data
        user_data = {
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'email': self.faker.email(),
            'role': 'Administrator'  # Removed is_active
        }
        
        # Create first user and verify success
        self.add_user_page.create_user(user_data)
        assert self.users_page.is_user_present(user_data['email']), \
            "First user creation failed"
        
        # Click New User button to create second user
        self.users_page.click(self.users_page.NEW_USER_BUTTON)
        
        # Try to create second user with same email
        duplicate_data = user_data.copy()
        duplicate_data.update({
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name()
        })
        
        self.add_user_page.fill_user_form(duplicate_data)
        self.add_user_page.save_user()
        
        # Verify correct error message appears using constants
        assert self.add_user_page.is_error_message_displayed(
            Constants.ERROR_MESSAGES["DUPLICATE_EMAIL"]
        ), "Duplicate email validation message not displayed"
