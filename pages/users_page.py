from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class UsersPage(BasePage):
    # Navigation and Page elements
    USERS_MENU_LINK = (By.XPATH, '//a[contains(@class, "sidebar__link") and .//span[text()="Users"]]')
    ADD_USER_BUTTON = (By.ID, 'add-user')
    DATA_TABLE = (By.ID, 'data-table')
    TABLE = (By.CSS_SELECTOR, '.table-responsive table')
    
    # Table headers and data
    NAME_HEADER = (By.XPATH, "//button[@data-button-type='1']")
    EMAIL_HEADER = (By.XPATH, "//button[@data-button-type='2']")
    ROLE_HEADER = (By.XPATH, "//button[@data-button-type='3']")
    STATUS_HEADER = (By.XPATH, "//button[@data-button-type='4']")
    USER_ROW = (By.CSS_SELECTOR, 'tbody tr')
    USER_NAME = (By.CSS_SELECTOR, 'td:nth-child(1)')
    USER_EMAIL = (By.CSS_SELECTOR, 'td:nth-child(2)')
    USER_ROLE = (By.CSS_SELECTOR, 'td:nth-child(3)')
    USER_STATUS = (By.CSS_SELECTOR, 'td:nth-child(4) .badge')
    EDIT_BUTTON = (By.CSS_SELECTOR, 'a.table__action[data-bs-title="Edit"]')

    # Pagination
    PAGINATION_NAV = (By.CLASS_NAME, 'pagy-nav')
    NEXT_PAGE = (By.CSS_SELECTOR, '.page.next a[data-turbo-action="advance"]')
    PREV_PAGE = (By.CSS_SELECTOR, '.page.prev:not(.disabled)')
    CURRENT_PAGE = (By.CSS_SELECTOR, '.page.active')
    PAGE_NUMBER_LINKS = (By.CSS_SELECTOR, '.page a[data-turbo-action="advance"]')

    # Success Messages
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert--soft-success .alert__content .col")
    
    def sort_by_column(self, column_type):
        """Sort table by column type (1=Name, 2=Email, 3=Role, 4=Status)"""
        button = self.find_element((By.XPATH, f"//button[@data-button-type='{column_type}']"))
        self.click((By.XPATH, f"//button[@data-button-type='{column_type}']"))
        return self

    def get_user_details(self, row):
        """Get all details for a user row"""
        return {
            'name': row.find_element(*self.USER_NAME).text,
            'email': row.find_element(*self.USER_EMAIL).text,
            'role': row.find_element(*self.USER_ROLE).text,
            'status': row.find_element(*self.USER_STATUS).text,
        }

    def get_all_users(self):
        """Get all users from current page"""
        users = []
        rows = self.find_elements(self.USER_ROW)
        for row in rows:
            users.append(self.get_user_details(row))
        return users

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
        """Find a user row by email, optionally checking all pages"""
        self.wait_for_users_table()  # Wait for table to load
        start_page = self.get_current_page_number()
        total_pages = self.get_total_pages()
        checked_pages = []
        
        while True:
            try:
                current_page = self.get_current_page_number()
                checked_pages.append(current_page)
                self.logger.info(f"Checking page {current_page} of {total_pages} for user {email}")
                
                # Wait for and get user rows
                users = self.wait.until(
                    EC.presence_of_all_elements_located(self.USER_ROW)
                )
                
                # Check each row
                for user in users:
                    try:
                        user_email = user.find_element(*self.USER_EMAIL).text
                        if user_email == email:
                            # Wait for row to be fully loaded
                            self.wait.until(
                                EC.presence_of_element_located(self.USER_ROLE)
                            )
                            return user
                    except:
                        continue
                
                # Try next page if needed
                if check_all_pages and current_page < total_pages:
                    if not self.click_next_page():
                        break
                else:
                    break
                    
            except Exception as e:
                self.logger.error(f"Error during user search: {str(e)}")
                break
        
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
        """Check if a user exists in the table (checks all pages)"""
        try:
            user = self.get_user_by_email(email, check_all_pages=True)
            exists = user is not None
            self.logger.info(f"User {email} {'found' if exists else 'not found'} in table")
            return exists
        except Exception as e:
            self.logger.error(f"Error checking for user {email}: {str(e)}")
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
