import pytest
from pages.edit_category_page import EditCategoryPage
from pages.categories_page import CategoriesPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from data.constants import AddCategoryPage as Constants
import logging
from faker import Faker  # Add this import

class TestEditCategory:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.faker = Faker()  # Initialize Faker
        self.driver = driver
        self.edit_page = EditCategoryPage(driver)
        self.categories_page = CategoriesPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        
        # Login and create test category
        self.driver.get(f"{config.base_url}/login")
        self.login_page.login(config.username, config.password)
        
        # Create test category for editing
        self.test_category = {
            "name": f"Test Category {self.faker.company()}",
            "description": self.faker.paragraph(),
            "sort_order": self.faker.random_int(min=1, max=999),
            "active": True
        }
        
        # Navigate and create category
        self.side_menu.navigate_to_system_settings_item('categories')
        self.categories_page.click_new_category()
        self.edit_page.upload_photo()
        self.edit_page.fill_category_form(**self.test_category)
        self.edit_page.save_category()
        
        yield
        
        # Cleanup: Could add cleanup code here if needed

    def test_edit_category_successful(self):
        """Test editing an existing category"""
        try:
            # Search and edit created category
            self.categories_page.search_category(self.test_category["name"])
            self.categories_page.edit_category(self.test_category["name"])
            
            # Verify existing data
            assert self.edit_page.verify_existing_data(self.test_category)
            
            # Update category data
            updated_data = {
                "name": f"{self.test_category['name']} Updated",
                "description": f"{self.test_category['description']} Updated",
                "sort_order": self.test_category["sort_order"] + 1,
                "active": False
            }
            
            # Ensure gallery is closed before proceeding
            self.edit_page.close_gallery()
            
            # Change photo and update fields
            self.edit_page.change_photo()
            
            # Ensure gallery is closed before form fill
            self.edit_page.close_gallery()
            
            self.edit_page.fill_category_form(**updated_data)
            self.edit_page.save_category()
            
            # Verify updates in table
            self.categories_page.search_category(updated_data["name"])
            categories = self.categories_page.get_all_categories()
            assert len(categories) > 0, "Updated category not found"
            
            updated_category = categories[0]
            assert updated_category["name"] == updated_data["name"]
            assert updated_category["sort_order"] == str(updated_data["sort_order"])
            assert updated_category["status"] == "Inactive"
            
            self.logger.info("Category updated and verified successfully")
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise

    def test_edit_category_validation(self):
        """Test validation when editing category"""
        try:
            # Navigate to edit page
            self.categories_page.search_category(self.test_category["name"])
            self.categories_page.edit_category(self.test_category["name"])
            
            # Clear fields and try to save
            self.edit_page.clear_form()
            self.edit_page.save_category()
            
            # Verify validation messages
            alert_errors = self.edit_page.get_error_messages()
            for error in [
                Constants.VALIDATION["NAME_REQUIRED"],
                Constants.VALIDATION["DESCRIPTION_REQUIRED"],
                Constants.VALIDATION["SORT_ORDER_REQUIRED"]
            ]:
                assert error in alert_errors, f"Missing validation message: {error}"
                
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise
