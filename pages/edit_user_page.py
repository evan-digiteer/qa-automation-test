from selenium.webdriver.common.by import By
from .add_user_page import AddUserPage
from selenium.webdriver.support.select import Select
from data.constants import ValidationData

class EditUserPage(AddUserPage):
    # Additional Messages
    SUCCESS_MESSAGE = ValidationData.USER_MESSAGES["USER_UPDATED"]
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert--soft-success")

    def get_current_data(self):
        """Get current form data"""
        return {
            'first_name': self.find_element(self.FIRST_NAME_INPUT).get_attribute('value'),
            'last_name': self.find_element(self.LAST_NAME_INPUT).get_attribute('value'),
            'email': self.find_element(self.EMAIL_INPUT).get_attribute('value'),
            'role': Select(self.find_element(self.ROLE_SELECT)).first_selected_option.text,
            'is_active': self.find_element(self.STATUS_TOGGLE).is_selected()
        }

    def verify_success_message(self):
        """Verify success message for update"""
        try:
            alert = self.find_element(self.SUCCESS_ALERT)
            return alert.is_displayed() and self.SUCCESS_MESSAGE in alert.text
        except:
            return False

    def clear_form_fields(self):
        """Clear name fields before updating"""
        self.find_element(self.FIRST_NAME_INPUT).clear()
        self.find_element(self.LAST_NAME_INPUT).clear()
        return self

    def update_user(self, updated_data):
        """Update user with new data"""
        self.clear_form_fields()  # Clear fields first
        self.fill_user_form(updated_data)
        self.save_user()
        return updated_data

    def fill_user_form(self, user_data):
        """Override fill_user_form to clear email field first"""
        if user_data.get('email'):
            self.find_element(self.EMAIL_INPUT).clear()
        return super().fill_user_form(user_data)
