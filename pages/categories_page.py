from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait  # Add this import
from .base_page import BasePage
from data.constants import CategoryPage

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
    CATEGORY_NAME = (By.CSS_SELECTOR, f"td:nth-child({CategoryPage.TableColumns.NAME})")
    SORT_ORDER = (By.CSS_SELECTOR, f"td:nth-child({CategoryPage.TableColumns.SORT_ORDER})")
    STATUS = (By.CSS_SELECTOR, f"td:nth-child({CategoryPage.TableColumns.STATUS}) .badge")
    ACTIONS = (By.CSS_SELECTOR, f"td:nth-child({CategoryPage.TableColumns.ACTION})")

    # Update column headers
    NAME_HEADER = (By.XPATH, f"//button[@data-button-type='{CategoryPage.TableColumns.NAME}']")
    SORT_ORDER_HEADER = (By.XPATH, f"//button[@data-button-type='{CategoryPage.TableColumns.SORT_ORDER}']")
    STATUS_HEADER = (By.XPATH, f"//button[@data-button-type='{CategoryPage.TableColumns.STATUS}']")

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

    # Add Delete Modal Elements
    DELETE_BUTTON = (By.CSS_SELECTOR, "a[data-action='click->admin--table#deleteItem']")
    DELETE_MODAL = (By.ID, "modalDelete")
    DELETE_MODAL_TITLE = (By.CLASS_NAME, "modal-title")
    KEEP_RECORD_BUTTON = (By.CSS_SELECTOR, "button[data-bs-dismiss='modal']")
    CONFIRM_DELETE_BUTTON = (By.ID, "jsDeleteItem")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button.modal-close")
    
    # Update Delete Modal Elements with more precise locators
    DELETE_MODAL = (By.ID, "modalDelete")
    MODAL_DIALOG = (By.CSS_SELECTOR, "#modalDelete .modal-dialog")
    DELETE_CONFIRM_TEXT = (By.CSS_SELECTOR, ".modal-body p")
    KEEP_RECORD_BUTTON = (By.CSS_SELECTOR, "button.btn--primary[data-bs-dismiss='modal']")
    CONFIRM_DELETE_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--outline-danger[data-turbo-method='delete']")

    # Add no records locator
    NO_RECORDS = (By.CSS_SELECTOR, "td.text-danger.text-center[colspan='8']")

    # Add error alert locator
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert.alert--danger .alert__content .col")

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
        """Search for a category by name with improved waits"""
        try:
            self.logger.info(f"Searching for category: {name}")
            
            # Wait for search input and clear it
            search_input = self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))
            search_input.clear()
            
            # Type search term
            search_input.send_keys(name)
            
            # Wait for search results with longer timeout
            long_wait = WebDriverWait(self.driver, 20)
            
            # Wait for table update
            old_rows = self.find_elements(self.TABLE_ROWS)
            if old_rows:
                # Wait for first row to become stale
                long_wait.until(EC.staleness_of(old_rows[0]))
            
            # Wait for new rows and table to be visible
            table = long_wait.until(EC.presence_of_element_located(self.TABLE))
            long_wait.until(EC.visibility_of(table))
            long_wait.until(EC.presence_of_element_located(self.TABLE_ROWS))
            
            # Additional wait for data to load
            self.driver.implicitly_wait(2)
            
            # Verify search results
            def verify_search_result():
                rows = self.find_elements(self.TABLE_ROWS)
                for row in rows:
                    if row.find_element(*self.CATEGORY_NAME).text.strip() == name:
                        return True
                return False

            # Wait up to 10 seconds for category to appear
            long_wait.until(lambda d: verify_search_result())
            self.logger.info(f"Category '{name}' found in search results")
            
            return self
            
        except Exception as e:
            self.logger.error(f"Search failed: {str(e)}")
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
            
            # Wait for page to be fully loaded first
            self.wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for button to be clickable
            button = self.wait.until(EC.element_to_be_clickable(self.NEW_CATEGORY_BUTTON))
            
            # Get current URL before click
            original_url = self.driver.current_url
            
            # Click using JavaScript for reliability
            self.driver.execute_script("arguments[0].click();", button)
            
            # Wait for URL to change
            self.wait.until(EC.url_changes(original_url))
            
            # Wait for add category page to load
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            
            # Additional wait for all elements to be present
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card__content")))
            
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

    def wait_for_modal(self):
        """Wait for modal to be visible and interactive"""
        try:
            # Wait for modal with longer timeout
            long_wait = WebDriverWait(self.driver, 20)
            
            # Wait for both modal and dialog
            modal = long_wait.until(EC.presence_of_element_located(self.DELETE_MODAL))
            dialog = long_wait.until(EC.visibility_of_element_located(self.MODAL_DIALOG))
            
            # Wait for confirmation text
            long_wait.until(EC.visibility_of_element_located(self.DELETE_CONFIRM_TEXT))
            
            # Additional wait for animation
            self.driver.implicitly_wait(1)
            
            return True
        except Exception as e:
            self.logger.error(f"Modal not visible: {str(e)}")
            return False

    def delete_category(self, name):
        """Delete a category by name with error message check"""
        try:
            self.logger.info(f"Attempting to delete category: {name}")
            
            # Find and click delete button for category
            found = False
            rows = self.find_elements(self.TABLE_ROWS)
            for row in rows:
                if row.find_element(*self.CATEGORY_NAME).text.strip() == name:
                    delete_btn = row.find_element(*self.DELETE_BUTTON)
                    self.driver.execute_script("arguments[0].click();", delete_btn)
                    found = True
                    break
            
            if not found:
                self.logger.error(f"Category '{name}' not found")
                return False

            # Wait for modal
            if not self.wait_for_modal():
                return False

            # Click confirm delete
            confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_DELETE_BUTTON))
            self.driver.execute_script("arguments[0].click();", confirm_btn)
            
            # Check for error message immediately
            try:
                error_elem = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.ERROR_ALERT)
                )
                if error_elem.is_displayed() and error_elem.text:
                    self.logger.info(f"Cannot delete '{name}' - {error_elem.text}")
                    return False
            except:
                # No error found, continue with verification
                pass

            # Wait for modal to close and verify deletion
            self.wait.until(EC.invisibility_of_element_located(self.DELETE_MODAL))
            
            # Wait a moment and verify category is gone
            self.driver.implicitly_wait(2)
            remaining_rows = self.find_elements(self.TABLE_ROWS)
            for row in remaining_rows:
                if row.find_element(*self.CATEGORY_NAME).text.strip() == name:
                    self.logger.error(f"Category '{name}' still exists after deletion")
                    return False
                    
            self.logger.info(f"Category '{name}' successfully deleted")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete category: {str(e)}")
            return False

    def cancel_delete(self, name):
        """Cancel category deletion with improved modal handling"""
        try:
            # Find and click delete button
            found = False
            rows = self.find_elements(self.TABLE_ROWS)
            for row in rows:
                if row.find_element(*self.CATEGORY_NAME).text.strip() == name:
                    delete_btn = row.find_element(*self.DELETE_BUTTON)
                    self.driver.execute_script("arguments[0].click();", delete_btn)
                    found = True
                    break
                    
            if not found:
                self.logger.error(f"Category '{name}' not found")
                return False

            # Wait for modal
            if not self.wait_for_modal():
                return False
            
            # Click keep record
            keep_btn = self.wait.until(EC.element_to_be_clickable(self.KEEP_RECORD_BUTTON))
            self.driver.execute_script("arguments[0].click();", keep_btn)
            
            # Wait for modal to close
            self.wait.until(EC.invisibility_of_element_located(self.DELETE_MODAL))
            
            # Verify category still exists
            rows = self.find_elements(self.TABLE_ROWS)
            still_exists = any(
                row.find_element(*self.CATEGORY_NAME).text.strip() == name 
                for row in rows
            )
            
            if not still_exists:
                self.logger.error("Category disappeared after cancellation")
                return False
                
            self.logger.info(f"Successfully cancelled deletion of category '{name}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cancel delete: {str(e)}")
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

    def verify_no_records(self):
        """Verify no records found after search"""
        try:
            long_wait = WebDriverWait(self.driver, 20)
            return long_wait.until(lambda d: 
                len(d.find_elements(*self.TABLE_ROWS)) == 0 or
                d.find_elements(*self.NO_RECORDS)[0].text.strip() == "No record found"
            )
        except Exception as e:
            self.logger.error(f"Failed to verify no records: {str(e)}")
            return False
