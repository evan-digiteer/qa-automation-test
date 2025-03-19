import pytest
import logging
from faker import Faker
from faker.providers import DynamicProvider, internet
from pages.add_category_page import AddCategoryPage
from pages.categories_page import CategoriesPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from pages.careers_page import CareersPage
from data.constants import AddCategoryPage as Constants
from pages.add_careers_page import AddCareerPage
import random
import string
import os

class TestAddCareer:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        # Initialize logger
        self.logger = logging.getLogger(self.__class__.__name__)

        job_title_provider = DynamicProvider(
            provider_name="job_title",
            elements=["chef", "waiter", "cashier"]
        )
        department_provider = DynamicProvider(
            provider_name="department",
            elements=["cooking department", "finance department", "admin department"]
        )


        # Initialize other attributes
        self.faker = Faker()
        self.add_career_page = AddCareerPage(driver)
        self.career_page = CareersPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        self.faker.add_provider(job_title_provider)
        self.faker.add_provider(department_provider)
        self.faker.add_provider(internet)
        
        # Login and navigate to add category page
        self.driver.get(f"{self.config.base_url}/login")
        self.login_page.login(self.config.username, self.config.password)
        self.side_menu.expand_system_settings()
        self.side_menu.navigate_to_section('careers')
        self.career_page.click_new_career()

    def generate_test_data(self):
        """Generate test data using Faker"""
        return {
            'job_title': f"Test Career {self.faker.job_title()}",
            'department': f"Test Department {self.faker.department()}",
            'apply_link': self.faker.uri(),
            'area': 'Muntinlupa',
            'store_branch': 'Alabang Town Center',
            'job_description': self.faker.sentence(nb_words=100),
            'responsibility': self.faker.sentence(nb_words=100),
            'qualification': self.faker.sentence(nb_words=100),
        }

    def generate_invalid_data(self):
        """Generate invalid test data"""
        return {
            'job_title': "",
            'department': "",
            'apply_link': "",
            'area': 'Test Area',
            'store_branch': 'Test Store Branch',
            'job_description': self.faker.sentence(nb_words=100),
            'responsibility': self.faker.sentence(nb_words=100),
            'qualification': self.faker.sentence(nb_words=100),
        }

    def test_create_career_successful(self):
        """Test creating a new career and verify it in the table"""
        try:
            # Generate unique test data
            test_career = {
                'job_title': f"Test Career {self.faker.job_title()}",
                'department': f"Test Department {self.faker.department()}",
                'apply_link': self.faker.uri(),
                'area': 'Muntinlupa',
                'store_branch': 'Alabang Town Center',
                'job_description': self.faker.sentence(nb_words=100),
                'responsibility': self.faker.sentence(nb_words=100),
                'qualification': self.faker.sentence(nb_words=100),
            }
            
            self.logger.info(f"Using test data: {test_career}")
            
            # Navigate and fill form
            self.career_page.click_new_career()
            
            # Fill form (will clear fields first)
            self.add_career_page.fill_career_form(
                career_data=test_career, active=True
            )
            
            # Save and verify
            self.add_career_page.save_career()
            assert "/admin/careers" in self.driver.current_url

            self.logger.info("Career created. Okay na 'to!")
            
        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise