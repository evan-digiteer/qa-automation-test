import pytest
import logging
from faker import Faker
from pages.add_category_page import AddCategoryPage
from pages.categories_page import CategoriesPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from data.constants import AddCategoryPage as Constants
import random
import string
import os

class TestAddCategory:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        # Initialize logger
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize other attributes
        self.faker = Faker()
        self.add_category_page = AddCategoryPage(driver)
        self.categories_page = CategoriesPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        
        # Login and navigate to add category page
        self.driver.get(f"{self.config.base_url}/login")
        self.login_page.login(self.config.username, self.config.password)
        self.side_menu.expand_system_settings()
        self.side_menu.navigate_to_system_settings_item('categories')
        self.categories_page.click_new_category()

    def generate_test_data(self):
        """Generate test data using Faker"""
        return {
            'name': f"Test Category {self.faker.word().capitalize()}",
            'description': self.faker.sentence(nb_words=5),
            'sort_order': self.faker.random_int(min=0, max=1000)
        }

    def generate_invalid_data(self):
        """Generate invalid test data"""
        return {
            'name': '',  # Empty name
            'description': '',  # Empty description
            'sort_order': self.faker.word(),  # Invalid sort order (string instead of number)
        }

    def test_add_category_page_elements(self):
        """Verify all elements are present on add category page"""
        assert self.add_category_page.verify_page_loaded(), "Page elements verification failed"
        
        # Verify page title
        title = self.add_category_page.find_element(self.add_category_page.PAGE_TITLE).text
        assert title == Constants.TITLE, f"Wrong page title. Expected: {Constants.TITLE}, Got: {title}"
        
        # Verify photo dimensions text
        dimensions = self.add_category_page.find_element(self.add_category_page.PHOTO_DIMENSIONS).text
        assert dimensions == Constants.PHOTO_DIMENSIONS, "Wrong photo dimensions text"

    def test_create_category_successful(self):
        """Test creating a new category and verify it in the table"""
        try:
            # Generate unique test data
            unique_name = f"Test Category {self.faker.company()} {self.faker.random_int(min=100, max=999)}"
            test_category = {
                "name": unique_name,  # Company name with random number for uniqueness
                "description": f"{self.faker.paragraph(nb_sentences=3)}\n{self.faker.catch_phrase()}",
                "sort_order": self.faker.random_int(min=1, max=9999),
                "active": True
            }
            
            self.logger.info(f"Using test data: {test_category}")
            
            # Navigate and fill form
            self.categories_page.click_new_category()
            self.add_category_page.upload_photo()
            
            # Store sort order for comparison
            sort_order = str(test_category["sort_order"])
            self.logger.info(f"Using sort order: {sort_order}")
            
            # Fill form (will clear fields first)
            self.add_category_page.fill_category_form(
                name=test_category["name"],
                description=test_category["description"],
                sort_order=sort_order,
                active=test_category["active"]
            )
            
            # Save and verify
            self.add_category_page.save_category()
            assert "/admin/categories" in self.driver.current_url
            
            # Search and verify
            self.logger.info(f"Searching for category: {test_category['name']}")
            self.categories_page.search_category(test_category["name"])
            
            categories = self.categories_page.get_all_categories()
            assert len(categories) > 0, "No categories found after search"
            
            new_category = categories[0]
            assert new_category["name"] == test_category["name"], \
                f"Name mismatch. Expected: {test_category['name']}, Got: {new_category['name']}"
            assert new_category["sort_order"] == sort_order, \
                f"Sort order mismatch. Expected: {sort_order}, Got: {new_category['sort_order']}"
            assert new_category["status"] == "Active", \
                f"Status mismatch. Expected: Active, Got: {new_category['status']}"
            
            self.logger.info("Category created and verified successfully")
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise

    def test_required_fields_validation(self):
        """Test required fields validation"""
        # Try to save empty form
        self.add_category_page.save_category()
        
        # Verify error messages
        for field_id in ["category_name", "category_description", "category_sort_order"]:
            error = self.add_category_page.get_field_error(field_id)
            assert error == Constants.VALIDATION["REQUIRED"], \
                f"Wrong or missing error message for {field_id}"

    def test_discard_changes(self):
        """Test discarding changes when creating category"""
        # Navigate to new category page
        self.side_menu.navigate_to_system_settings_item('categories')
        self.categories_page.click_new_category()
        
        # Fill form but don't save
        self.add_category_page.fill_category_form(
            name="Discarded Category",
            description="This should not be saved",
            sort_order=99
        )
        
        # Click discard
        self.add_category_page.discard_changes()
        
        # Verify back on categories page
        assert "/admin/categories" in self.driver.current_url

    # ...rest of existing tests...
