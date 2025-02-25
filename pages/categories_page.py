from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from .base_page import BasePage

class CategoriesPage(BasePage):
    # Page Header Elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header span")
    NEW_CATEGORY_BUTTON = (By.CSS_SELECTOR, "a[href='/admin/categories/new']")
    
    # Search and Filter Elements
    SEARCH_INPUT = (By.ID, "name")
    SORT_SELECT = (By.NAME, "order_by")
    STATUS_FILTER = (By.NAME, "status")
    ITEMS_PER_PAGE = (By.NAME, "count_per_page")
    
    # Table Elements
    TABLE = (By.CSS_SELECTOR, ".table")
    TABLE_HEADERS = (By.CSS_SELECTOR, "thead th")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    
    # Table Column Elements
    CATEGORY_NAME = (By.CSS_SELECTOR, "td:nth-child(1)")
    SORT_ORDER = (By.CSS_SELECTOR, "td:nth-child(2)")
    STATUS = (By.CSS_SELECTOR, "td:nth-child(3) .badge")
    EDIT_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Edit']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Delete']")
    
    # Pagination Elements
    PAGINATION = (By.CSS_SELECTOR, "nav.pagy.nav")  # Updated class selector
    NEXT_PAGE = (By.CSS_SELECTOR, "nav.pagy a[aria-label='Next']:not([aria-disabled='true'])")
    PREV_PAGE = (By.CSS_SELECTOR, "nav.pagy a[aria-label='Previous']:not([aria-disabled='true'])")
    CURRENT_PAGE = (By.CSS_SELECTOR, "nav.pagy a.current")
    PAGE_LINKS = (By.CSS_SELECTOR, "nav.pagy a:not([aria-label])")
    
    # Update TomSelect locators to be more precise
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".ts-wrapper.single")  # Parent wrapper
    SORT_INPUT = (By.CSS_SELECTOR, ".ts-control")  # Clickable input area
    SORT_OPTIONS_LIST = (By.CSS_SELECTOR, ".ts-dropdown-content")  # Options container
    SORT_OPTION = (By.CSS_SELECTOR, 'div[data-selectable][data-value="{}"]')  # Option template

    # Add TomSelect locators for Status filter
    STATUS_DROPDOWN = (By.CSS_SELECTOR, "[data-controller='admin--tom-select'][name='status']")
    STATUS_WRAPPER = (By.CSS_SELECTOR, "select[name='status'] ~ .ts-wrapper")  # Changed to sibling selector
    STATUS_CONTROL = (By.CSS_SELECTOR, ".ts-control")  # More specific selector
    STATUS_DROPDOWN_CONTENT = (By.CSS_SELECTOR, ".ts-dropdown-content")
    STATUS_OPTION = (By.CSS_SELECTOR, "div[data-value='{}']")
    STATUS_OPTIONS = {
        True: (By.CSS_SELECTOR, "div[data-value='true'].option"),  # Active option
        False: (By.CSS_SELECTOR, "div[data-value='false'].option")  # Inactive option
    }
    
    def get_category_details(self, row):
        """Get details for a category row"""
        return {
            'name': row.find_element(*self.CATEGORY_NAME).text,
            'sort_order': row.find_element(*self.SORT_ORDER).text,
            'status': row.find_element(*self.STATUS).text
        }

    def get_all_categories(self):
        """Get all categories from current page"""
        categories = []
        rows = self.find_elements(self.TABLE_ROWS)
        for row in rows:
            categories.append(self.get_category_details(row))
        return categories

    def search_category(self, name):
        """Search for a category by name"""
        self.type(self.SEARCH_INPUT, name)
        # Wait for table to update
        self.wait.until(EC.staleness_of(self.find_element(self.TABLE_ROWS)))
        return self

    def sort_by(self, order):
        """Sort categories by given order using TomSelect dropdown"""
        try:
            self.logger.info(f"Attempting to sort by: {order}")
            
            # Find and click the dropdown to open it
            dropdown = self.wait.until(EC.presence_of_element_located(self.SORT_DROPDOWN))
            input_area = dropdown.find_element(*self.SORT_INPUT)
            self.driver.execute_script("arguments[0].click();", input_area)
            
            # Wait for dropdown content to be visible
            self.wait.until(EC.visibility_of_element_located(self.SORT_OPTIONS_LIST))
            
            # Find and click the specific option using JavaScript
            option_locator = (self.SORT_OPTION[0], self.SORT_OPTION[1].format(order))
            option = self.wait.until(EC.presence_of_element_located(option_locator))
            self.driver.execute_script("arguments[0].click();", option)
            
            # Wait for table to update
            old_rows = self.find_elements(self.TABLE_ROWS)
            if old_rows:
                # Wait for the first row to become stale
                self.wait.until(EC.staleness_of(old_rows[0]))
            
            # Wait for new rows
            self.wait.until(EC.presence_of_all_elements_located(self.TABLE_ROWS))
            
            # Additional wait for sorting to complete
            self.driver.implicitly_wait(1)
            
            return self
            
        except Exception as e:
            self.logger.error(f"Failed to sort table: {str(e)}")
            return self

    def filter_by_status(self, status):
        """Filter categories by status using TomSelect dropdown"""
        try:
            self.logger.info(f"Attempting to filter by status: {status}")
            
            # Find and wait for the wrapper
            wrapper = self.wait.until(EC.presence_of_element_located(self.STATUS_WRAPPER))
            
            # Find and click the control area to open dropdown
            control = wrapper.find_element(*self.STATUS_CONTROL)
            self.driver.execute_script("arguments[0].click();", control)
            
            # Wait for dropdown to be visible
            self.wait.until(EC.visibility_of_element_located(self.STATUS_DROPDOWN))
            
            # Find the specific option based on status
            option_locator = self.STATUS_OPTIONS[status]
            option = wrapper.find_element(*option_locator)
            self.logger.info(f"Clicking option with value: {status}")
            self.driver.execute_script("arguments[0].click();", option)
            
            # Wait for table update
            old_rows = self.find_elements(self.TABLE_ROWS)
            if old_rows:
                self.wait.until(EC.staleness_of(old_rows[0]))
            
            # Wait for new rows
            self.wait.until(EC.presence_of_all_elements_located(self.TABLE_ROWS))
            self.driver.implicitly_wait(1)  # Additional wait for data
            
            return self
            
        except Exception as e:
            self.logger.error(f"Failed to filter by status: {str(e)}")
            return self

    def set_items_per_page(self, count):
        """Set number of items per page"""
        self.select_by_value(self.ITEMS_PER_PAGE, str(count))
        return self

    def click_new_category(self):
        """Click new category button and wait for navigation"""
        try:
            self.logger.info("Attempting to navigate to new category page")
            
            # Wait for button to be clickable
            button = self.wait.until(EC.element_to_be_clickable(self.NEW_CATEGORY_BUTTON))
            
            # Get current URL before click
            original_url = self.driver.current_url
            
            # Click using JavaScript for reliability
            self.driver.execute_script("arguments[0].click();", button)
            
            # Wait for URL to change
            self.wait.until(EC.url_changes(original_url))
            
            # Additional wait for new page load
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            
            # Verify URL contains expected path
            current_url = self.driver.current_url
            self.logger.info(f"Navigated to: {current_url}")
            
            return self
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to new category page: {str(e)}")
            return self

    def edit_category(self, name):
        """Edit category by name"""
        rows = self.find_elements(self.TABLE_ROWS)
        for row in rows:
            if row.find_element(*self.CATEGORY_NAME).text == name:
                row.find_element(*self.EDIT_BUTTON).click()
                return True
        return False

    def delete_category(self, name):
        """Delete category by name"""
        rows = self.find_elements(self.TABLE_ROWS)
        for row in rows:
            if row.find_element(*self.CATEGORY_NAME).text == name:
                row.find_element(*self.DELETE_BUTTON).click()
                return True
        return False

    def has_pagination(self):
        """Check if pagination is present and has multiple pages"""
        try:
            pagination = self.find_element(self.PAGINATION)
            return pagination.is_displayed() and len(self.find_elements(self.PAGE_LINKS)) > 1
        except:
            return False

    def get_current_page_number(self):
        """Get current page number"""
        try:
            current = self.find_element(self.CURRENT_PAGE)
            return int(current.text)
        except:
            return 1

    def navigate_to_page(self, direction):
        """Navigate to next or previous page"""
        try:
            if direction == 'next':
                button = self.find_element(self.NEXT_PAGE)
            else:
                button = self.find_element(self.PREV_PAGE)
                
            # Get current categories before navigation
            current_categories = self.get_all_categories()
            
            # Click the pagination button
            self.driver.execute_script("arguments[0].click();", button)
            
            # Wait for table update
            self.wait.until(EC.staleness_of(self.find_element(self.TABLE_ROWS)))
            self.wait.until(EC.presence_of_element_located(self.TABLE_ROWS))
            
            # Additional wait for data
            self.driver.implicitly_wait(1)
            
            return current_categories
            
        except Exception as e:
            self.logger.error(f"Failed to navigate {direction}: {str(e)}")
            return None
