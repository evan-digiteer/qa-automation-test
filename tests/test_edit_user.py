import pytest
from pages.users_page import UsersPage
from pages.edit_user_page import EditUserPage
from pages.add_user_page import AddUserPage
from pages.login_page import LoginPage
from data.constants import ValidationData, URLs
from datetime import datetime

class TestEditUser:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.users_page = UsersPage(driver)
        self.edit_user_page = EditUserPage(driver)
        self.add_user_page = AddUserPage(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        
        # Login first
        self.driver.get(self.config.base_url + URLs.LOGIN_PAGE)
        self.login_page.login(self.config.username, self.config.password)
        self.users_page.navigate_to_users()

    @pytest.fixture
    def test_user(self):
        """Create a test user for editing"""
        # Navigate to add user page
        self.users_page.click(self.users_page.ADD_USER_BUTTON)
        
        # Create test user with known data
        test_data = {
            'first_name': self.add_user_page.faker.first_name(),
            'last_name': self.add_user_page.faker.last_name(),
            'email': self.add_user_page.faker.email(),
            'role': ValidationData.USER_ROLES[0],
            'is_active': True
        }
        
        self.add_user_page.create_user(test_data)
        self.users_page.navigate_to_users()
        
        # Verify user was created
        assert self.users_page.is_user_present(test_data['email']), \
            "Test user creation failed"
            
        return test_data

    def test_edit_user_details(self, test_user):
        """Test editing user details"""
        # Navigate to edit page
        assert self.users_page.edit_user(test_user['email']), "Failed to navigate to edit page"
        
        # Update only the names with 'Updated' marker
        updated_data = test_user.copy()
        updated_data.update({
            'first_name': f"Updated {test_user['first_name']}",  # Add 'Updated' marker
            'last_name': test_user['last_name']  # Keep original last name
        })
        
        # Update user
        self.edit_user_page.update_user(updated_data)
        
        # Verify success message and updated user exists
        assert self.users_page.verify_success_message(ValidationData.USER_MESSAGES["USER_UPDATED"]), \
            "Success message not shown after redirect"
        
        # Get user row and verify update
        user_row = self.users_page.get_user_by_email(test_user['email'])
        assert user_row is not None, f"Updated user {test_user['email']} not found"
        
        # Verify name contains "Updated" marker
        actual_name = user_row.find_element(*self.users_page.USER_NAME).text
        assert "Updated" in actual_name, \
            f"Name does not contain 'Updated' marker: {actual_name}"

    def test_edit_validation(self, test_user):
        """Test edit form validation"""
        self.users_page.edit_user(test_user['email'])
        
        # Clear required fields
        self.edit_user_page.find_element(self.edit_user_page.FIRST_NAME_INPUT).clear()
        self.edit_user_page.find_element(self.edit_user_page.LAST_NAME_INPUT).clear()
        self.edit_user_page.save_user()
        
        assert self.edit_user_page.is_error_message_displayed(), \
            "Required field validation messages not displayed"

