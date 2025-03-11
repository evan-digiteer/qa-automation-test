import pytest
import logging
from pages.categories_page import CategoriesPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from data.constants import CategoryPage

class TestCategories:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.categories_page = CategoriesPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Login and navigate to categories
        self.driver.get(f"{self.config.base_url}/login")
        self.login_page.login(self.config.username, self.config.password)
        self.side_menu.expand_system_settings()
        self.side_menu.navigate_to_system_settings_item('categories')

    def test_categories_page_elements(self):
        """Verify basic page elements are present and correct"""
        # Get actual values
        actual_title = self.categories_page.find_element(self.categories_page.PAGE_TITLE).text
        is_new_button_visible = self.categories_page.find_element(self.categories_page.NEW_CATEGORY_BUTTON).is_displayed()
        is_table_visible = self.categories_page.find_element(self.categories_page.TABLE).is_displayed()
        
        # Assertions with clear messages using constants
        assert actual_title == CategoryPage.TITLE, \
            f"Page title mismatch. Expected: '{CategoryPage.TITLE}', Got: '{actual_title}'"
        assert is_new_button_visible, "New Category button is not visible"
        assert is_table_visible, "Categories table is not visible"

    def test_search_functionality(self):
        """Test category search functionality with known data"""
        # Test data
        test_category = "Featured"  # Using a known category name
        
        # Perform search
        self.categories_page.search_category(test_category)
        
        # Get actual results
        found_categories = self.categories_page.get_all_categories()
        matching_categories = [cat for cat in found_categories if test_category in cat['name']]
        
        # Assertions
        assert len(matching_categories) > 0, \
            f"No categories found containing name '{test_category}'. Found categories: {[c['name'] for c in found_categories]}"
        
        # Verify each matching category
        for category in matching_categories:
            assert test_category in category['name'], \
                f"Found category '{category['name']}' does not contain search term '{test_category}'"

    def test_sort_by_order(self):
        """Test sorting functionality"""
        def verify_sort_order(categories, descending=False):
            orders = [int(cat['sort_order']) for cat in categories]
            self.logger.info(f"Current sort order: {orders}")
            
            for i in range(len(orders) - 1):
                current, next_val = orders[i], orders[i + 1]
                if descending:
                    assert current >= next_val, \
                        f"Sort order not in descending order.\nFull order: {orders}\nFound {current} before {next_val}"
                else:
                    assert current <= next_val, \
                        f"Sort order not in ascending order.\nFull order: {orders}\nFound {current} before {next_val}"

        # Test descending order
        self.logger.info("Testing sort order descending")
        self.categories_page.sort_by_column(CategoryPage.TableColumns.SORT_ORDER)
        self.driver.implicitly_wait(1)
        verify_sort_order(self.categories_page.get_all_categories(), descending=True)

        # Test ascending order
        self.logger.info("Testing sort order ascending")
        self.categories_page.sort_by(CategoryPage.SORT_OPTIONS["ORDER_ASC"])
        self.driver.implicitly_wait(1)
        verify_sort_order(self.categories_page.get_all_categories(), descending=False)

    def test_sort_by_name(self):
        """Test sorting by name"""
        def verify_name_sequence(names, descending=False):
            """Verify names are in roughly correct sequence (A-Z or Z-A)"""
            self.logger.info(f"Checking name order: {names}")
            first = names[0].lower()
            last = names[-1].lower()
            
            if descending:
                # In Z-A order, first should be "greater" than last
                assert first > last, \
                    f"Names not in Z-A order. First: '{first}' should come after Last: '{last}'"
            else:
                # In A-Z order, first should be "less" than last
                assert first < last, \
                    f"Names not in A-Z order. First: '{first}' should come before Last: '{last}'"
            return True

        # Test A-Z name sorting
        self.logger.info("Testing Category Name A-Z")
        self.categories_page.sort_by_column(CategoryPage.TableColumns.NAME)
        self.driver.implicitly_wait(1)
        categories = self.categories_page.get_all_categories()
        names_asc = [cat['name'] for cat in categories]
        assert verify_name_sequence(names_asc, descending=False), \
            f"Names not sorted A-Z: {names_asc}"

        # Test Z-A name sorting
        self.logger.info("Testing Category Name Z-A")
        self.categories_page.sort_by(CategoryPage.SORT_OPTIONS["NAME_DESC"])
        self.driver.implicitly_wait(1)
        categories = self.categories_page.get_all_categories()
        names_desc = [cat['name'] for cat in categories]
        assert verify_name_sequence(names_desc, descending=True), \
            f"Names not sorted Z-A: {names_desc}"

    def test_filter_by_status(self):
        """Test status filtering for both active and inactive"""
        # Test active filter
        self.logger.info("Testing Active status filter")
        self.categories_page.filter_by_status(True)
        self.driver.implicitly_wait(1)  # Wait for filter to apply
        active_categories = self.categories_page.get_all_categories()
        
        # Log the results for debugging
        self.logger.info(f"Found {len(active_categories)} active categories")
        for cat in active_categories:
            self.logger.info(f"Category: {cat['name']}, Status: {cat['status']}")
        
        # Verify active filter
        assert all(cat['status'] == CategoryPage.STATUS["ACTIVE"] for cat in active_categories), \
            f"Found non-active categories in active filter: {[cat for cat in active_categories if cat['status'] != CategoryPage.STATUS['ACTIVE']]}"
        
        # Test inactive filter
        self.logger.info("Testing Inactive status filter")
        self.categories_page.filter_by_status(False)
        self.driver.implicitly_wait(1)  # Wait for filter to apply
        inactive_categories = self.categories_page.get_all_categories()
        
        # Log the results for debugging
        self.logger.info(f"Found {len(inactive_categories)} inactive categories")
        for cat in inactive_categories:
            self.logger.info(f"Category: {cat['name']}, Status: {cat['status']}")
        
        # Verify inactive filter
        assert all(cat['status'] == CategoryPage.STATUS["INACTIVE"] for cat in inactive_categories), \
            f"Found active categories in inactive filter: {[cat for cat in inactive_categories if cat['status'] != CategoryPage.STATUS['INACTIVE']]}"

    def test_items_per_page(self):
        """Test items per page functionality with different values"""
        for items in CategoryPage.ITEMS_PER_PAGE_OPTIONS:
            # Set items per page
            self.categories_page.set_items_per_page(items)
            
            # Get actual count
            categories = self.categories_page.get_all_categories()
            actual_count = len(categories)
            
            # Assertion
            assert actual_count <= items, \
                f"Too many items shown. Expected max {items}, but got {actual_count} items"
            
            self.logger.info(f"Successfully verified {actual_count} items shown when limit is {items}")

    def test_new_category_navigation(self):
        """Test navigation to new category form"""
        # Click new category button
        self.categories_page.click_new_category()
        
        # Wait for URL to update and page to load
        self.driver.implicitly_wait(2)
        
        # Get actual URL
        actual_url = self.driver.current_url
        expected_url = CategoryPage.URLS["NEW"]
        
        # Assertion using constant with better error message
        assert expected_url in actual_url, \
            f"Navigation failed.\nExpected URL to contain: '{expected_url}'\nActual URL: '{actual_url}'\nDifference at: {actual_url.find(expected_url)}"

    def test_pagination(self):
        """Test pagination functionality"""
        # First set items per page to minimum to ensure pagination
        self.categories_page.set_items_per_page('10')
        self.driver.implicitly_wait(2)  # Wait for table update
        
        # Check if pagination exists and has multiple pages
        if not self.categories_page.has_pagination():
            self.logger.info("Not enough categories to test pagination")
            return
        
        # Get initial page data
        initial_categories = self.categories_page.get_all_categories()
        initial_page = self.categories_page.get_current_page_number()
        self.logger.info(f"Starting from page {initial_page} with {len(initial_categories)} categories")
        
        # Store first page categories
        first_page_categories = {cat['name'] for cat in initial_categories}
        
        # Navigate to next page
        second_page_categories = self.categories_page.navigate_to_page('next')
        if second_page_categories:
            # Verify different categories on second page
            current_categories = {cat['name'] for cat in self.categories_page.get_all_categories()}
            assert not first_page_categories.intersection(current_categories), \
                "Found duplicate categories between pages"
            
            # Navigate back
            returned_categories = self.categories_page.navigate_to_page('prev')
            if returned_categories:
                # Verify we're back to original categories
                final_categories = {cat['name'] for cat in self.categories_page.get_all_categories()}
                assert final_categories == first_page_categories, \
                    f"Categories don't match after returning to first page.\nExpected: {first_page_categories}\nGot: {final_categories}"
        
        # Verify final page number
        final_page = self.categories_page.get_current_page_number()
        assert final_page == initial_page, f"Did not return to initial page. Started at {initial_page}, ended at {final_page}"
