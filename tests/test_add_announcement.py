import pytest
import logging
from faker import Faker
from selenium.webdriver.support.wait import WebDriverWait

from pages.add_announcement_page import AddAnnouncementPage
from pages.announcements_page import AnnouncementsPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from data.constants import AddAnnouncementPage as Constants
import random
import string
import os


class TestAddAnnouncement:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        # Initialize logger
        self.logger = logging.getLogger(self.__class__.__name__)

        # Initialize other attributes
        self.faker = Faker()
        self.add_announcement_page = AddAnnouncementPage(driver)
        self.announcements_page = AnnouncementsPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config

        # Login and navigate to add announcement page
        self.driver.get(f"{self.config.base_url}/login")
        self.login_page.login(self.config.username, self.config.password)
        self.side_menu.expand_system_settings()
        self.side_menu.navigate_to_section('announcements')
        self.announcements_page.click_new_announcement()

    def generate_test_data(self):
        """Generate test data"""
        return {
            'headline': f"Test Headline {self.faker.word().capitalize()} {self.faker.random_int(min=100, max=999)}",
            'description': self.faker.sentence(nb_words=10),
            'content': self.faker.paragraph(nb_sentences=3),
            'author': self.faker.name(),
            'announcement_category': "KC CATEGORY",
            'date': None,
            'active': True,
            'featured': True,
            'show_ribbon': True
        }

    def generate_invalid_data(self):
        """Generate invalid test data"""
        return {
            'headline': '',  # Empty headline
            'description': '',  # Empty description
            'content': '',  # Empty content
            'author': '',  # Empty author
            'announcement_category': 'Invalid Category',  # Non-existent announcement category
            'date': None,
            'active': 'yes',  # Should be boolean
            'featured': 'maybe',  # Should be boolean
            'show_ribbon': 'null'  # Should be boolean
        }

    def test_add_announcement_page_elements(self):
        """Verify all elements are present on add announcement page"""
        assert self.add_announcement_page.verify_page_loaded(), "Page elements verification failed"

        # Verify page title
        title = self.add_announcement_page.find_element(self.add_announcement_page.PAGE_TITLE).text
        assert title == Constants.TITLE, f"Wrong page title. Expected: {Constants.TITLE}, Got: {title}"

        # Verify photo dimensions text
        dimensions = self.add_announcement_page.find_element(self.add_announcement_page.PHOTO_DIMENSIONS).text
        assert dimensions == Constants.PHOTO_DIMENSIONS, "Wrong photo dimensions text"

    def test_create_announcement_successful(self):
        """Test creating a new announcement and verify it in the table"""
        try:
            test_announcement = self.generate_test_data()

            self.logger.info(f"Using test data: {test_announcement}")

            # Navigate and fill form
            self.announcements_page.click_new_announcement()
            self.add_announcement_page.upload_photo()

            # Fill form
            self.add_announcement_page.fill_announcement_form(
                headline=test_announcement["headline"],
                description=test_announcement["description"],
                content=test_announcement["content"],
                author=test_announcement["author"],
                announcement_category=test_announcement["announcement_category"],
                date=test_announcement["date"],
                active=test_announcement["active"],
                featured=test_announcement["featured"],
                show_ribbon=test_announcement["show_ribbon"]
            )

            # Save and verify
            self.add_announcement_page.save_announcement()
            assert "/admin/announcements" in self.driver.current_url

            # Search and verify
            self.logger.info(f"Searching for announcement: {test_announcement['headline']}")
            self.announcements_page.search_announcement(test_announcement["headline"])

            announcements = self.announcements_page.get_all_announcements()
            assert len(announcements) > 0, "No announcements found after search"

            new_announcement = announcements[0]
            assert new_announcement["headline"] == test_announcement["headline"], \
                f"Headline mismatch. Expected: {test_announcement['headline']}, Got: {new_announcement['headline']}"
            assert new_announcement["status"] == "Active", \
                f"Status mismatch. Expected: Active, Got: {new_announcement['status']}"

            self.logger.info("Announcement created and verified successfully")

        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise

    def test_required_fields_validation(self):
        """Test form validation for required fields"""
        try:
            # Use the page's clear form method
            self.add_announcement_page.clear_form()

            # Try to save empty form
            self.add_announcement_page.save_announcement()

            # Check alert error messages (notification box)
            alert_errors = self.add_announcement_page.get_error_messages()
            self.logger.info(f"Alert errors: {alert_errors}")

            expected_alerts = [
                Constants.VALIDATION["PHOTO_REQUIRED"],
                Constants.VALIDATION["HEADLINE_REQUIRED"],
                Constants.VALIDATION["DESCRIPTION_REQUIRED"],
                Constants.VALIDATION["CONTENT_REQUIRED"],
                Constants.VALIDATION["AUTHOR_REQUIRED"],
                Constants.VALIDATION["DATE_REQUIRED"]
            ]
            for error in expected_alerts:
                assert error in alert_errors, f"Missing alert error: {error}"

            # Check inline field errors (under input fields)
            field_errors = self.add_announcement_page.get_all_field_errors()
            self.logger.info(f"Field errors: {field_errors}")

            expected_fields = {
                Constants.FIELDS["HEADLINE"]["LABEL"]: Constants.INLINE_VALIDATION["HEADLINE_REQUIRED"],
                Constants.FIELDS["PHOTO"]["LABEL"]: Constants.INLINE_VALIDATION["PHOTO_REQUIRED"],
                Constants.FIELDS["DESCRIPTION"]["LABEL"]: Constants.INLINE_VALIDATION["DESCRIPTION_REQUIRED"],
                Constants.FIELDS["AUTHOR"]["LABEL"]: Constants.INLINE_VALIDATION["AUTHOR_REQUIRED"],
                Constants.FIELDS["DATE"]["LABEL"]: Constants.INLINE_VALIDATION["DATE_REQUIRED"],
                Constants.FIELDS["CONTENT"]["LABEL"]: Constants.INLINE_VALIDATION["CONTENT_REQUIRED"]
            }

            assert field_errors == expected_fields, \
                f"Field error mismatch. Expected: {expected_fields}, Got: {field_errors}"

        except Exception as e:
            self.logger.error(f"Test failed due to exception: {str(e)}")
            raise

    def test_discard_changes(self):
        """Test discarding changes when creating an announcement"""
        # Navigate to the announcements page
        self.side_menu.navigate_to_section('announcements')
        self.announcements_page.click_new_announcement()

        self.add_announcement_page.fill_announcement_form(
            headline="Discarded Announcement",
            description="This should not be saved",
            content="This content should also be discarded",
            author="Test Author",
            announcement_category="KC CATEGORY",
            date=None
        )

        # Click discard
        self.add_announcement_page.discard_changes()

        # Verify back on announcements page
        assert "/admin/announcements" in self.driver.current_url

