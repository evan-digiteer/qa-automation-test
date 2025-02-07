from selenium.webdriver.common.by import By
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
    PAGINATION = (By.CLASS_NAME, 'pagy-nav')
    NEXT_PAGE = (By.CSS_SELECTOR, '.page.next a')
    PREV_PAGE = (By.CSS_SELECTOR, '.page.prev')

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

    def has_next_page(self):
        """Check if there's a next page"""
        try:
            return self.find_element(self.NEXT_PAGE).is_displayed()
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

    def get_user_by_email(self, email):
        """Find a user row by email"""
        users = self.get_user_rows()
        for user in users:
            user_email = user.find_element(*self.USER_EMAIL).text
            if user_email == email:
                return user
        return None

    def is_user_present(self, email):
        """Check if a user exists in the table"""
        return bool(self.get_user_by_email(email))

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
        """Wait for users table to be loaded"""
        self.logger.info("Waiting for users table to load")
        return self.find_element(self.TABLE)

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
