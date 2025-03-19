from datetime import datetime

import pytest
from pages.announcements_page import AnnouncementsPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from pages.add_announcement_page import AddAnnouncementPage
from data.constants import AnnouncementsPage as Constants
import logging
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class TestDeleteAnnouncements:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.faker = Faker()
        self.driver = driver
        self.announcements_page = AnnouncementsPage(driver)
        self.add_page = AddAnnouncementPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)

        # Login and create test announcement
        self.driver.get(f"{config.base_url}/login")
        self.login_page.login(config.username, config.password)

        # Create test announcement
        self.test_announcement = {
            'headline': f"Test Headline {self.faker.word().capitalize()} {self.faker.random_int(min=100, max=999)}",
            'description': self.faker.sentence(nb_words=10),
            'content': self.faker.paragraph(nb_sentences=3),
            'author': self.faker.name(),
            'announcement_category': "KC CATEGORY",
            'date': datetime.today().strftime("%B %d, %Y"),
            'active': True,
            'featured': True,
            'show_ribbon': True
        }

        # Navigate and create announcement
        self.side_menu.navigate_to_section('announcements')
        self.announcements_page.click_new_announcement()
        self.add_page.upload_photo()
        self.add_page.fill_announcement_form(**self.test_announcement)
        self.add_page.save_announcement()

        yield

        # No cleanup needed as we're testing deletion

    def test_delete_announcement_successful(self):
        """Test successful announcement deletion"""
        try:
            # Navigate back to announcements page first
            self.side_menu.navigate_to_section('announcements')

            # Search for created announcement
            self.announcements_page.search_announcement(self.test_announcement["headline"])

            # Delete announcement
            assert self.announcements_page.delete_announcement(self.test_announcement["headline"]), \
                "Failed to delete announcement"

            # Wait for page to reload after deletion
            self.driver.refresh()

            # Search again and verify no results
            self.announcements_page.search_announcement(self.test_announcement["headline"])
            assert self.announcements_page.verify_no_records(), \
                "Announcement still exists after deletion"

            self.logger.info("Announcement verified as deleted - no records found")

        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise

    def test_cancel_announcement_deletion(self):
        """Test canceling announcement deletion"""
        try:
            # Search for created announcement
            self.announcements_page.search_announcement(self.test_announcement["headline"])

            # Start deletion but cancel
            assert self.announcements_page.cancel_delete(self.test_announcement["headline"]), \
                "Failed to cancel deletion"

            # Verify announcement still exists
            self.announcements_page.search_announcement(self.test_announcement["headline"])
            announcements = self.announcements_page.get_all_announcements()
            assert any(cat["headline"] == self.test_announcement["headline"] for cat in announcements), \
                "Announcement was deleted despite cancellation"

            self.logger.info("Announcement deletion cancelled successfully")

        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise