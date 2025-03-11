from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
from data.constants import UsersPage as Constants

# Define column indices outside class
NAME_COL = Constants.TableColumns.NAME
EMAIL_COL = Constants.TableColumns.EMAIL
ROLE_COL = Constants.TableColumns.ROLE
ACTION_COL = Constants.TableColumns.ACTION

class UsersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # Page Header Elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header span")
    NEW_USER_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--primary[href='/admin/users/new']")
    
    # Search and Filter Elements - Update to match actual HTML
    NAME_SEARCH = (By.CSS_SELECTOR, "input.field.field--search[placeholder='Search by User Name']")
    EMAIL_SEARCH = (By.CSS_SELECTOR, "input.field.field--search[placeholder='Search by User Email']")
    
    # TomSelect Elements - Update with correct IDs and structure
    NAME_SORT = (By.ID, "tomselect-1")
    EMAIL_SORT = (By.ID, "tomselect-2")
    ITEMS_PER_PAGE_SELECT = (By.ID, "tomselect-3")
    
    SORT_DROPDOWNS = {
        'name': {
            'container': (By.CSS_SELECTOR, "#tomselect-1-ts-control"),
            'options': (By.CSS_SELECTOR, "#tomselect-1-ts-dropdown .ts-dropdown-content"),
            'clear': (By.CSS_SELECTOR, "#tomselect-1-ts-control .clear-button")
        },
        'email': {
            'container': (By.CSS_SELECTOR, "#tomselect-2-ts-control"),
            'options': (By.CSS_SELECTOR, "#tomselect-2-ts-dropdown .ts-dropdown-content"),
            'clear': (By.CSS_SELECTOR, "#tomselect-2-ts-control .clear-button")
        },
        'items': {
            'container': (By.CSS_SELECTOR, "#tomselect-3-ts-control"),
            'options': (By.CSS_SELECTOR, "#tomselect-3-ts-dropdown .ts-dropdown-content"),
            'value': (By.CSS_SELECTOR, "#tomselect-3-ts-control .item")
        }
    }
    
    # Table Elements
    TABLE = (By.CSS_SELECTOR, ".table")
    TABLE_HEADERS = (By.CSS_SELECTOR, "thead th")
    TABLE_ROWS = (By.CSS_SELECTOR, "tbody tr")
    
    # User Row Elements using predefined column indices
    USER_NAME_COL = (By.CSS_SELECTOR, f"td:nth-child({NAME_COL})")
    USER_EMAIL_COL = (By.CSS_SELECTOR, f"td:nth-child({EMAIL_COL})")
    USER_ROLE_COL = (By.CSS_SELECTOR, f"td:nth-child({ROLE_COL})")
    USER_ACTIONS_COL = (By.CSS_SELECTOR, f"td:nth-child({ACTION_COL})")
    
    # User Details Elements
    USER_AVATAR = (By.CSS_SELECTOR, ".avatar.avatar--6.avatar--rounded img")
    USER_NAME = (By.CSS_SELECTOR, ".d-inline-flex span")
    USER_EMAIL = (By.CSS_SELECTOR, "td a[href^='mailto:']")
    USER_ROLE = (By.CSS_SELECTOR, "td:nth-child(3)")
    
    # Action Buttons
    VIEW_BUTTON = (By.CSS_SELECTOR, "a.table__action[data-bs-title='View']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "a.table__action[data-action='click->admin--table#deleteItem']")
    
    # Pagination Elements
    PAGINATION = (By.CSS_SELECTOR, ".pagy.nav")
    NEXT_PAGE = (By.CSS_SELECTOR, ".pagy a[aria-label='Next']:not([aria-disabled='true'])")
    PREV_PAGE = (By.CSS_SELECTOR, ".pagy a[aria-label='Previous']:not([aria-disabled='true'])")
    CURRENT_PAGE = (By.CSS_SELECTOR, ".pagy a[aria-current='page']")
    PAGE_LINKS = (By.CSS_SELECTOR, ".pagy a:not([aria-label])")
    
    # Delete Modal Elements
    DELETE_MODAL = (By.ID, "modalDelete")
    DELETE_MODAL_TITLE = (By.CSS_SELECTOR, ".modal-title")
    KEEP_RECORD_BUTTON = (By.CSS_SELECTOR, "button.btn--primary[data-bs-dismiss='modal']")
    CONFIRM_DELETE_BUTTON = (By.ID, "jsDeleteItem")
    
    # Records Count Element
    RECORDS_COUNT = (By.CSS_SELECTOR, ".overline strong")
    
    # Navigation and Page elements
    USERS_MENU_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link") and .//span[text()="Users"]]')
    ADD_USER_BUTTON = (By.ID, 'add-user')
    DATA_TABLE = (By.ID, 'data-table')
    
    # Table headers using predefined column indices
    NAME_HEADER = (By.XPATH, f"//button[@data-button-type='{NAME_COL}']")
    EMAIL_HEADER = (By.XPATH, f"//button[@data-button-type='{EMAIL_COL}']")
    ROLE_HEADER = (By.XPATH, f"//button[@data-button-type='{ROLE_COL}']")
    STATUS_HEADER = (By.XPATH, "//button[@data-button-type='4']")
    USER_ROW = (By.CSS_SELECTOR, 'tbody tr')
    USER_STATUS = (By.CSS_SELECTOR, 'td:nth-child(4) .badge')
    EDIT_BUTTON = (By.CSS_SELECTOR, 'a.table__action[data-bs-title="Edit"]')

    # Pagination
    PAGINATION_NAV = (By.CLASS_NAME, 'pagy-nav')
    PAGE_NUMBER_LINKS = (By.CSS_SELECTOR, '.page a[data-turbo-action="advance"]')

    # Success Messages
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert--soft-success .alert__content .col")
    
    def sort_by_column(self, column_type):
        """Sort table by column type (1=Name, 2=Email, 3=Role, 4=Status)"""
        button = self.find_element((By.XPATH, f"//button[@data-button-type='{column_type}']"))
        self.click((By.XPATH, f"//button[@data-button-type='{column_type}']"))
        return self

    def get_user_details(self, row):
        """Get details for a user row with retry mechanism"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return {
                    'name': self.driver.execute_script("return arguments[0].querySelector('td:nth-child(1) span').textContent;", row),
                    'email': self.driver.execute_script("return arguments[0].querySelector('td:nth-child(2) a').textContent;", row),
                    'role': self.driver.execute_script("return arguments[0].querySelector('td:nth-child(3)').textContent;", row)
                }
            except Exception as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to get user details after {max_retries} attempts: {str(e)}")
                    raise
                self.logger.warning(f"Retry {attempt + 1}: Failed to get user details")
                self.wait_for_users_table()

    def get_all_users(self):
        """Get all users from current page with stability check"""
        try:
            # Wait for table to be ready
            self.wait_for_users_table()
            self.driver.implicitly_wait(1)  # Short wait for data to settle
            
            # Get all rows with retry mechanism
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    rows = self.find_elements(self.USER_ROW)
                    return [self.get_user_details(row) for row in rows]
                except Exception as e:
                    if attempt == max_retries - 1:
                        self.logger.error(f"Failed to get users after {max_retries} attempts: {str(e)}")
                        raise
                    self.logger.warning(f"Retry {attempt + 1}: Failed to get users")
                    self.wait_for_users_table()
                    
        except Exception as e:
            self.logger.error(f"Failed to get all users: {str(e)}")
            return []

    def get_active_users(self):
        """Get only active users"""
        return [user for user in self.get_all_users() if 'Active' in user['status']]

    def get_inactive_users(self):
        """Get only inactive users"""
        return [user for user in self.get_all_users() if 'Inactive' in user['status']]

    def get_current_page_number(self):
        """Get current page number"""
        try:
            return int(self.find_element(self.CURRENT_PAGE).text)
        except:
            return 1

    def get_total_pages(self):
        """Get total number of pages"""
        try:
            # Get all page links including both numbers and next/prev
            page_links = self.find_elements((By.CSS_SELECTOR, '.pagy-nav .page'))
            # Filter to only numbered pages (exclude next/prev)
            numbered_pages = [link for link in page_links if link.text.isdigit()]
            if numbered_pages:
                return max([int(link.text) for link in numbered_pages])
            return 1
        except Exception as e:
            self.logger.error(f"Error getting total pages: {str(e)}")
            return 1

    def has_next_page(self):
        """Check if there's a next page"""
        try:
            return bool(self.find_element(self.NEXT_PAGE))
        except:
            return False

    def has_previous_page(self):
        """Check if there's a previous page"""
        try:
            return bool(self.find_element(self.PREV_PAGE))
        except:
            return False

    def navigate_to_users(self):
        """Navigate to Users page via sidebar menu"""
        self.logger.info("Navigating to Users page")
        self.click(self.USERS_MENU_LINK)
        return self

    def get_user_rows(self):
        """Get all user rows from the table"""
        return self.find_elements(self.USER_ROW)

    def get_user_by_email(self, email, check_all_pages=True):
        """Find a user row by email with improved waits and retries"""
        try:
            self.logger.info(f"Looking for user with email: {email}")
            
            # Wait for table with longer timeout
            long_wait = WebDriverWait(self.driver, 30)
            long_wait.until(EC.presence_of_element_located(self.TABLE))
            long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr')))
            
            # Additional wait for data to settle
            self.driver.implicitly_wait(3)
            
            # Get all user rows
            rows = self.find_elements(self.USER_ROW)
            for row in rows:
                try:
                    user_email = row.find_element(*self.USER_EMAIL_COL).text.strip()
                    self.logger.info(f"Checking user with email: {user_email}")
                    if user_email == email:
                        self.logger.info(f"Found user: {email}")
                        return row
                except Exception as e:
                    self.logger.warning(f"Error checking row: {str(e)}")
                    continue
            
            self.logger.warning(f"User not found: {email}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error searching for user: {str(e)}")
            return None

    def click_next_page(self):
        """Click next page if available"""
        try:
            if self.has_next_page():
                self.logger.info("Clicking next page button")
                # Wait for and find the next page link
                next_button = self.wait.until(
                    EC.element_to_be_clickable(self.NEXT_PAGE)
                )
                # Get the href attribute
                next_url = next_button.get_attribute('href')
                self.logger.info(f"Navigating to: {next_url}")
                # Use driver.get() instead of click()
                self.driver.get(next_url)
                self.wait_for_users_table()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to navigate to next page: {str(e)}")
            return False

    def is_user_present(self, email):
        """Check if a user exists in the table with better search handling"""
        try:
            self.logger.info(f"Checking for user: {email}")
            
            # Try direct search first
            self.search_user(email, search_type="email")
            
            # Wait for search results with longer timeout
            long_wait = WebDriverWait(self.driver, 20)
            
            # Wait for table update
            long_wait.until(EC.presence_of_element_located(self.TABLE))
            long_wait.until(EC.presence_of_element_located(self.USER_ROW))
            
            # Additional wait for data
            self.driver.implicitly_wait(3)
            
            # Check rows after search
            rows = self.find_elements(self.USER_ROW)
            for row in rows:
                user_email = row.find_element(*self.USER_EMAIL_COL).text.strip()
                self.logger.info(f"Found email in row: {user_email}")
                if user_email == email:
                    self.logger.info(f"User found: {email}")
                    return True
            
            self.logger.warning(f"User not found after search: {email}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error verifying user presence: {str(e)}")
            return False

    def click_user_row(self, email):
        """Click on a user row by email"""
        user_row = self.get_user_by_email(email)
        if user_row:
            self.logger.info(f"Clicking user row with email: {email}")
            user_row.click()
            return True
        self.logger.warning(f"User with email {email} not found in table")
        return False

    def wait_for_users_table(self):
        """Wait for users table to be loaded and ready"""
        self.logger.info("Waiting for users table to load")
        self.wait.until(
            EC.presence_of_element_located(self.TABLE)
        )
        self.wait.until(
            EC.presence_of_element_located(self.USER_ROW)
        )
        return True

    def is_on_users_page(self):
        """Verify we're on the Users page"""
        return (self.find_element(self.TABLE).is_displayed() and 
                self.find_element(self.ADD_USER_BUTTON).is_displayed())

    def edit_user(self, email):
        """Click edit button for specific user"""
        try:
            user_row = self.get_user_by_email(email)
            if user_row:
                edit_link = user_row.find_element(*self.EDIT_BUTTON)
                self.logger.info(f"Clicking edit button for user: {email}")
                edit_link.click()
                return True
            self.logger.warning(f"User with email {email} not found")
            return False
        except Exception as e:
            self.logger.error(f"Failed to click edit button: {str(e)}")
            return False

    def verify_success_message(self, expected_message=None):
        """Verify success message is displayed and contains expected text"""
        try:
            alert = self.find_element(self.SUCCESS_ALERT)
            if alert.is_displayed():
                alert_text = alert.text.strip()
                self.logger.info(f"Found success message: {alert_text}")
                if expected_message:
                    # More flexible check since message includes dynamic user info
                    return expected_message.split()[0] in alert_text
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error checking success message: {str(e)}")
            return False

    def select_items_per_page(self, count):
        """Select number of items per page using TomSelect"""
        try:
            # Click dropdown to open
            dropdown = self.wait.until(EC.element_to_be_clickable(
                self.SORT_DROPDOWNS['items']['container']
            ))
            self.driver.execute_script("arguments[0].click();", dropdown)
            
            # Wait for options and click desired value
            option = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"div[data-value='{count}']")
            ))
            self.driver.execute_script("arguments[0].click();", option)
            
            # Wait for table update
            self.wait_for_users_table()
            return True
        except Exception as e:
            self.logger.error(f"Failed to set items per page: {str(e)}")
            return False

    def search_user(self, query, search_type="name"):
        """Search for a user by name or email with improved waits"""
        try:
            self.logger.info(f"Searching for user by {search_type}: {query}")
            
            # Select correct search input based on search type
            search_locator = self.NAME_SEARCH if search_type == "name" else self.EMAIL_SEARCH
            
            # Wait for search input and clear it
            search_input = self.wait.until(EC.presence_of_element_located(search_locator))
            search_input.clear()
            
            # Type search term
            search_input.send_keys(query)
            
            # Use longer timeout for search results
            long_wait = WebDriverWait(self.driver, 20)
            
            # Wait for old results to become stale
            old_rows = self.find_elements(self.TABLE_ROWS)
            if old_rows:
                long_wait.until(EC.staleness_of(old_rows[0]))
            
            # Wait for table and new results
            table = long_wait.until(EC.presence_of_element_located(self.TABLE))
            long_wait.until(EC.visibility_of(table))
            long_wait.until(EC.presence_of_element_located(self.TABLE_ROWS))
            
            # Additional wait for data to settle
            self.driver.implicitly_wait(2)
            
            # Verify search results
            def verify_search_result():
                rows = self.find_elements(self.TABLE_ROWS)
                for row in rows:
                    if search_type == "name":
                        text = row.find_element(*self.USER_NAME).text.strip()
                    else:
                        text = row.find_element(*self.USER_EMAIL).text.strip()
                    if text == query:
                        return True
                return False
            
            # Wait for matching result
            long_wait.until(lambda d: verify_search_result())
            self.logger.info(f"User with {search_type} '{query}' found in results")
            
            return self
            
        except Exception as e:
            self.logger.error(f"Search failed: {str(e)}")
            return self
