from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait  # Add this import
from .base_page import BasePage
from data.constants import CategoryPage

class CareersPage(BasePage):
    # Page Header Elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header span")
    NEW_CAREER_BUTTON = (By.CSS_SELECTOR, "a[href='/admin/careers/new']")
    
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

    def click_new_career(self):
        """Click new career button and wait for navigation"""
        try:
            self.logger.info("Attempting to navigate to new career page")
            
            # Wait for page to be fully loaded first
            self.wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for button to be clickable
            button = self.wait.until(EC.element_to_be_clickable(self.NEW_CAREER_BUTTON))
            
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
            self.logger.error(f"Failed to navigate to new career page: {str(e)}")
            return self