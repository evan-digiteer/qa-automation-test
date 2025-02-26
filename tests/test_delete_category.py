import pytest
from pages.categories_page import CategoriesPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from pages.add_category_page import AddCategoryPage
from data.constants import CategoryPage as Constants
import logging
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class TestDeleteCategory:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.faker = Faker()
        self.driver = driver
        self.categories_page = CategoriesPage(driver)
        self.add_page = AddCategoryPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        
        # Login and create test category
        self.driver.get(f"{config.base_url}/login")
        self.login_page.login(config.username, config.password)
        
        # Create test category
        self.test_category = {
            "name": f"Test Delete Category {self.faker.company()}",
            "description": self.faker.paragraph(),
            "sort_order": self.faker.random_int(min=1, max=999),
            "active": True
        }
        
        # Navigate and create category
        self.side_menu.navigate_to_system_settings_item('categories')
        self.categories_page.click_new_category()
        self.add_page.upload_photo()
        self.add_page.fill_category_form(**self.test_category)
        self.add_page.save_category()
        
        yield
        
        # No cleanup needed as we're testing deletion

    def test_delete_category_successful(self):
        """Test successful category deletion"""
        try:
            # Navigate back to categories page first
            self.side_menu.navigate_to_system_settings_item('categories')
            
            # Search for created category
            self.categories_page.search_category(self.test_category["name"])
            
            # Delete category
            assert self.categories_page.delete_category(self.test_category["name"]), \
                "Failed to delete category"
                
            # Wait for page to reload after deletion
            self.driver.refresh()
            
            # Search again and verify no results
            self.categories_page.search_category(self.test_category["name"])
            assert self.categories_page.verify_no_records(), \
                "Category still exists after deletion"
            
            self.logger.info("Category verified as deleted - no records found")
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise

    def test_cancel_category_deletion(self):
        """Test canceling category deletion"""
        try:
            # Search for created category
            self.categories_page.search_category(self.test_category["name"])
            
            # Start deletion but cancel
            assert self.categories_page.cancel_delete(self.test_category["name"]), \
                "Failed to cancel deletion"
                
            # Verify category still exists
            self.categories_page.search_category(self.test_category["name"])
            categories = self.categories_page.get_all_categories()
            assert any(cat["name"] == self.test_category["name"] for cat in categories), \
                "Category was deleted despite cancellation"
                
            self.logger.info("Category deletion cancelled successfully")
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise
