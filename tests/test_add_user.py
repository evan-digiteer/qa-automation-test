import pytest
from pages.users_page import UsersPage
from pages.add_user_page import AddUserPage
from pages.login_page import LoginPage
from data.constants import ValidationData, URLs

class TestAddUser:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.users_page = UsersPage(driver)
        self.add_user_page = AddUserPage(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        
        # Login and navigate to users page
        self.driver.get(self.config.base_url + URLs.LOGIN_PAGE)
        self.login_page.login(self.config.username, self.config.password)
        self.users_page.navigate_to_users()
        
        # Click add user button
        self.users_page.click(self.users_page.ADD_USER_BUTTON)

    def test_create_user_with_valid_data(self):
        """Test creating a new user with valid data"""
        # Create user with generated data
        user_data = self.add_user_page.create_user()
        
        # Verify user appears in the table
        assert self.users_page.is_user_present(user_data['email']), \
            f"New user {user_data['email']} not found in users table"

    def test_discard_user_creation(self):
        """Test discarding user creation"""
        # Fill form but don't save
        user_data = self.add_user_page.fill_user_form()
        self.add_user_page.discard_changes()
        
        # Verify back on users page and user not created
        assert self.users_page.is_on_users_page(), "Not returned to users page"
        assert not self.users_page.is_user_present(user_data['email']), \
            f"User {user_data['email']} should not exist after discard"

    def test_required_fields_validation(self):
        """Test required fields validation"""
        self.add_user_page.click(self.add_user_page.SAVE_BUTTON)
        assert self.add_user_page.is_error_message_displayed(), \
            "Required field validation message not displayed"

    @pytest.mark.parametrize("role", ValidationData.USER_ROLES)
    def test_user_role_selection(self, role):
        """Test creating users with different roles"""
        # Generate test data
        user_data = {
            'first_name': self.add_user_page.faker.first_name(),
            'last_name': self.add_user_page.faker.last_name(),
            'email': self.add_user_page.faker.email(),
            'role': role,
            'is_active': True
        }
        
        # Create user and navigate back to users page
        self.add_user_page.create_user(user_data)
        self.users_page.navigate_to_users()
        
        # Find user and verify role
        user_row = self.users_page.get_user_by_email(user_data['email'])
        assert user_row is not None, f"User {user_data['email']} not found in table"
        
        user_role = user_row.find_element(*self.users_page.USER_ROLE).text
        assert user_role == role, f"User role mismatch. Expected: {role}, Got: {user_role}"
