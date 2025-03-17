from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from .base_page import BasePage

class AddCareerPage(BasePage):
    #Form Elements
    CAREER_FORM = (By.ID, "new career")
    FORM_ERROR_STREAM = (By.ID, "formErrorStream")

    # Header Elements
    TITLE = (By.CSS_SELECTOR, ".card__header .fw-bold")
    BACK_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Back']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.btn.btn--success")
    DISCARD_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--outline-danger[href='/admin/careers']")

     # Input Fields and Toggle switch
    ACTIVE_SWITCH = (By.ID, "career_active")
    JOB_TITLE_INPUT = (By.ID, "career_job_title")
    DEPARTMENT_INPUT = (By.ID, "career_department")
    APPLY_LINK_INPUT = (By.ID, "career_apply_link")
    
     # AREA AND STORE BRANCH DROPDOWNS
    AREA_SELECT = (By.ID, "career_area_id")
    AREA_DROPDOWN = (By.CSS_SELECTOR, ".ts-wrapper.single")
    AREA_INPUT = (By.CSS_SELECTOR, ".ts-control")
    AREA_OPTIONS = (By.CSS_SELECTOR, ".ts-dropdown-content")
    STORE_BRANCH_SELECT = (By.ID, "career_store_branch_id")
    STORE_DROPDOWN = (By.CSS_SELECTOR, "#store-branch-field .ts-wrapper.single")
    STORE_INPUT = (By.CSS_SELECTOR, "#store-branch-field .ts-control")
    AREA_OPTIONS = (By.CSS_SELECTOR, "#store-branch-field .ts-dropdown-content")

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def fill_user_form(self, career_data=None, active=True):
        """Fill user form with provided data or generate fake data"""
        if career_data is None:
            career_data = {
                'job_title': 'Chef',
                'department': 'Baking',
                'apply_link': 'www.google.com',
                'area' : 'Muntinlupa',
                'store_branch' : "Alabang Town Center"
            }

        # Set active status
        if active != self.find_element(self.ACTIVE_SWITCH).is_selected():
            self.click(self.ACTIVE_SWITCH)
        
        self.type(self.JOB_TITLE_INPUT, career_data['job_title'])
        self.type(self.DEPARTMENT_INPUT, career_data['department'])
        self.type(self.APPLY_LINK_INPUT, career_data['apply_link'])
        
        # Handle role selection
        area_select = Select(self.find_element(self.AREA_SELECT))
        area_select.select_by_visible_text(career_data['area'])
        store_branch_select = Select(self.find_element(self.STORE_BRANCH_SELECT))
        store_branch_select.select_by_visible_text(career_data['store_branch'])
        
        
        return career_data
