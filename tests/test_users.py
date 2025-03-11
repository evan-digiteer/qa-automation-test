import pytest
import logging
from faker import Faker
from pages.users_page import UsersPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from data.constants import LoginPage as LoginConstants
from data.constants import UsersPage as Constants  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random

class TestUsers:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.faker = Faker()
        
        # Initialize pages
        self.users_page = UsersPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        
        # Login first
        self.logger.info("Logging in before user tests")
        self.driver.get(f"{config.base_url}{LoginConstants.URLS['LOGIN']}")
        assert self.login_page.login(config.username, config.password), "Login failed"
        self.logger.info("Successfully logged in")
        
        # Navigate to users page using specific method
        self.logger.info("Navigating to Users page")
        assert self.side_menu.navigate_to_users(), "Failed to navigate to Users page"
        
        # Wait for users table to load
        assert self.users_page.wait_for_users_table(), "Users table failed to load"
        self.logger.info("Users page loaded successfully")

    def test_users_page_elements(self):
        """Test basic page elements are present"""
        self.logger.info("Verifying Users page elements")
        
        # Verify title
        title = self.users_page.find_element(self.users_page.PAGE_TITLE).text
        self.logger.info(f"Found page title: {title}")
        assert title == Constants.TITLE, \
            f"Wrong page title\nExpected: {Constants.TITLE}\nActual: {title}"
        
        # Verify table headers
        headers = [th.text for th in self.users_page.find_elements(self.users_page.TABLE_HEADERS)]
        self.logger.info(f"Found table headers: {headers}")
        assert headers == Constants.TABLE_HEADERS, \
            f"Table headers mismatch\nExpected: {Constants.TABLE_HEADERS}\nActual: {headers}"
        
        # Verify action buttons
        assert self.users_page.find_element(self.users_page.NEW_USER_BUTTON).is_displayed(), \
            "New User button not visible"
            
        assert self.users_page.find_element(self.users_page.TABLE).is_displayed(), \
            "Users table not visible"
        
        self.logger.info("All page elements verified successfully")

    def test_user_search_by_name(self):
        """Test search functionality by name with random existing user"""
        users = self.users_page.get_all_users()
        if not users:
            pytest.skip("No users available to test search functionality")
        
        test_user = random.choice(users)
        self.logger.info(f"Testing name search with user: {test_user['name']}")
        
        self.users_page.search_user(test_user['name'], search_type="name")
        
        results = self.users_page.get_all_users()
        assert len(results) > 0, "No results found for name search"
        assert any(r['name'] == test_user['name'] for r in results), \
            f"User '{test_user['name']}' not found in search results"
        
        self.logger.info("Name search test completed successfully")

    def test_user_search_by_email(self):
        """Test search functionality by email with random existing user"""
        users = self.users_page.get_all_users()
        if not users:
            pytest.skip("No users available to test search functionality")
        
        test_user = random.choice(users)
        self.logger.info(f"Testing email search with user: {test_user['email']}")
        
        self.users_page.search_user(test_user['email'], search_type="email")
        
        results = self.users_page.get_all_users()
        assert len(results) > 0, "No results found for email search"
        assert any(r['email'] == test_user['email'] for r in results), \
            f"User with email '{test_user['email']}' not found in search results"
        
        self.logger.info("Email search test completed successfully")

    def test_pagination_navigation(self):
        """Test pagination if available"""
        # Set to 10 items per page to ensure pagination
        assert self.users_page.select_items_per_page(10), "Failed to set items per page"
        
        # Get initial page data
        first_page_users = self.users_page.get_all_users()
        total_records = first_page_users[0]  # First row
        
        if self.users_page.has_next_page():
            # Store first user for comparison
            first_user = first_page_users[0]["email"]
            
            # Navigate to next page
            assert self.users_page.click_next_page(), "Failed to navigate to next page"
            
            # Get new page data and verify different content
            second_page_users = self.users_page.get_all_users()
            assert all(user["email"] != first_user for user in second_page_users), \
                "Found duplicate users between pages"
                
            # Verify page navigation in URL
            assert "page=2" in self.driver.current_url, \
                f"URL doesn't show correct page. URL: {self.driver.current_url}"
            
            self.logger.info("Pagination navigation successful")
        else:
            self.logger.info("Not enough users to test pagination")

