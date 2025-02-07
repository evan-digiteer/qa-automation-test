import pytest
from pages.users_page import UsersPage
from pages.login_page import LoginPage
from data.constants import URLs

class TestUsers:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.users_page = UsersPage(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        
        # Login first using URLs constant
        login_url = self.config.base_url + URLs.LOGIN_PAGE
        self.driver.get(login_url)
        self.login_page.login(self.config.username, self.config.password)
        
        # Navigate to users page
        self.users_page.navigate_to_users()

    def test_users_page_elements(self):
        """Test basic page elements are present"""
        assert self.users_page.is_on_users_page(), "Not on Users page"
        assert self.users_page.find_element(self.users_page.ADD_USER_BUTTON).is_displayed(), "Add User button not visible"
        assert self.users_page.find_element(self.users_page.TABLE).is_displayed(), "Users table not visible"

    @pytest.mark.parametrize("column_type,column_name", [
        ("1", "Name"),
        ("2", "Email"),
        ("3", "Role"),
        ("4", "Status")
    ])
    def test_column_sorting(self, column_type, column_name):
        """Test sorting functionality for each column"""
        self.users_page.sort_by_column(column_type)
        self.users_page.logger.info(f"Tested sorting for {column_name} column")

    def test_user_filtering(self):
        """Test filtering users by status"""
        active_users = self.users_page.get_active_users()
        inactive_users = self.users_page.get_inactive_users()
        
        assert len(active_users) + len(inactive_users) == len(self.users_page.get_all_users()), \
            "Sum of active and inactive users should equal total users"

    def test_edit_user_link(self):
        """Test edit user functionality"""
        users = self.users_page.get_all_users()
        if users:
            first_user_email = users[0]['email']
            assert self.users_page.edit_user(first_user_email), \
                f"Failed to click edit for user: {first_user_email}"

    def test_pagination_if_available(self):
        """Test pagination if available"""
        if self.users_page.has_next_page():
            self.users_page.click(self.users_page.NEXT_PAGE)
            assert self.users_page.wait_for_users_table(), "Table not loaded after pagination"

