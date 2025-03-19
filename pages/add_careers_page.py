from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from faker import Faker
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
    JOB_DESCRIPTION_INPUT = (By.XPATH, "/html/body/main/div/form/div/div/div[4]/div/div[7]/div[1]/div/div[2]/div[1]/p")
    RESPONSIBILITIES_INPUT = (By.XPATH, "/html/body/main/div/form/div/div/div[4]/div/div[8]/div[1]/div/div[2]/div[1]/p")
    QUALIFICATIONS_INPUT = (By.ID,  "/html/body/main/div/form/div/div/div[4]/div/div[9]/div[1]/div/div[2]/div[1]/p")
    
     # AREA AND STORE BRANCH DROPDOWNS
    AREA_SELECT = (By.ID, "career_area_id")
    AREA_DROPDOWN = (By.CSS_SELECTOR, ".ts-wrapper.single")
    AREA_INPUT = (By.CSS_SELECTOR, ".ts-control")
    AREA_OPTIONS = (By.CSS_SELECTOR, ".ts-dropdown-content")
    STORE_BRANCH_SELECT = (By.ID, "career_store_branch_id")
    STORE_DROPDOWN = (By.CSS_SELECTOR, "#store-branch-field .ts-wrapper.single")
    STORE_INPUT = (By.CSS_SELECTOR, "#store-branch-field .ts-control")
    STORE_OPTIONS = (By.CSS_SELECTOR, "#store-branch-field .ts-dropdown-content")

    # Field Groups
    FIELD_GROUP = (By.CLASS_NAME, "field-group")
    FIELD_CONTAINER = (By.CLASS_NAME, "field-container")
    FIELD_HELPER = (By.CLASS_NAME, "field-helper")
    REQUIRED_LABEL = (By.CLASS_NAME, "label--required")

    

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def fill_career_form(self, career_data=None, active=True):
        """Fill career form with provided data or generate fake data"""
        if career_data is None:
            career_data = {
                'job_title': 'Chef',
                'department': 'Baking',
                'apply_link': 'www.google.com',
                'area' : 'Muntinlupa',
                'store_branch' : "Alabang Town Center",
                'job_description' : "can cook",
                'responsibility' : "cook in the kitchen",
                'qualification' : "college degree",

            }

        # Set active status
        if active != self.find_element(self.ACTIVE_SWITCH).is_selected():
            self.click(self.ACTIVE_SWITCH)
        
        self.type(self.JOB_TITLE_INPUT, career_data['job_title'])
        self.type(self.DEPARTMENT_INPUT, career_data['department'])
        self.type(self.APPLY_LINK_INPUT, career_data['apply_link'])
        # self.type(self.JOB_DESCRIPTION_INPUT,career_data['job_description'] )
        # self.type(self.RESPONSIBILITIES_INPUT, career_data['responsibility'])
        # self.type(self.QUALIFICATIONS_INPUT,career_data['qualification'])
        
        # Handle role selection
        area_select = Select(self.find_element(self.AREA_SELECT))
        area_select.select_by_visible_text(career_data['area'])
        store_branch_select = Select(self.find_element(self.STORE_BRANCH_SELECT))
        store_branch_select.select_by_visible_text(career_data['store_branch'])
        
        return career_data
    
    def save_career(self):
        """Click save button and wait for redirect"""
        try:
            self.logger.info("Saving new career")
            current_url = self.driver.current_url
            
            # Click save button
            self.click(self.SAVE_BUTTON)
            
            # Wait for URL to change with longer timeout
            long_wait = WebDriverWait(self.driver, 30)  # Increased timeout
            long_wait.until(EC.url_contains('/admin/careers'))
            long_wait.until(lambda d: d.current_url != current_url)
            
            # Wait for page load and table
            long_wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.table')))
            long_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr')))
            
            # Extra wait for data to settle
            self.driver.implicitly_wait(3)
            
            self.logger.info("Career saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save career: {str(e)}")
            return False
        
        
    def create_career(self, career_data=None):
        """Complete flow to create a new career"""
        filled_data = self.fill_career_form(career_data)
        self.save_career()
        return filled_data
    
    
