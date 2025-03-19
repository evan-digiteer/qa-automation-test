from datetime import datetime
import pytest
from pages.edit_announcement_page import EditAnnouncementPage
from pages.announcements_page import AnnouncementsPage
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from data.constants import AddAnnouncementPage as Constants
import logging
from faker import Faker  # Add this import


class TestEditAnnouncement:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.faker = Faker()  # Initialize Faker
        self.driver = driver
        self.edit_page = EditAnnouncementPage(driver)
        self.announcements_page = AnnouncementsPage(driver)
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)

        # Login and create test announcement
        self.driver.get(f"{config.base_url}/login")
        self.login_page.login(config.username, config.password)

        # Create test category
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

        # Navigate and create category
        self.side_menu.navigate_to_section('announcements')
        self.announcements_page.click_new_announcement()
        self.edit_page.upload_photo()
        self.edit_page.fill_announcement_form(**self.test_announcement)
        self.edit_page.save_announcement()

        yield

        # Cleanup: Could add cleanup code here if needed

    def test_edit_announcement_successful(self):
        """Test editing an existing announcement"""
        try:
            # Search and edit created announcement
            self.announcements_page.search_announcement(self.test_announcement["headline"])
            self.announcements_page.edit_announcement(self.test_announcement["headline"])

            # Wait for page load before verification
            assert self.edit_page.wait_for_page_load(), "Edit page failed to load"

            # First verify existing data
            assert self.edit_page.verify_existing_data(self.test_announcement), "Data verification failed"

            updated_data = {
                "headline": f"{self.test_announcement['headline']} Updated",
                "description": f"{self.test_announcement['description']} Updated",
                "content": f"{self.test_announcement['content']} Updated",
                "author": self.test_announcement["author"],
                "announcement_category": self.test_announcement["announcement_category"],
                "date": self.test_announcement["date"],  # Assuming no change
                "active": False,
                "featured": False,
                "show_ribbon": False
            }

            # Fill form with updated data
            assert self.edit_page.fill_announcement_form(**updated_data), "Form fill failed"

            # Save changes
            assert self.edit_page.save_announcement(), "Save failed"

            # Verify updates in table
            self.announcements_page.search_announcement(updated_data["headline"])
            announcements = self.announcements_page.get_all_announcements()
            assert len(announcements) > 0, "Updated announcement not found"

            updated_announcement = announcements[0]
            assert updated_announcement["headline"] == updated_data["headline"]
            assert updated_announcement["status"] == "Inactive"

            self.logger.info("Announcement updated and verified successfully")

        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise

    def test_edit_announcement_validation(self):
        """Test validation when editing an announcement"""
        try:
            # Navigate to edit page
            self.announcements_page.search_announcement(self.test_announcement["headline"])
            self.announcements_page.edit_announcement(self.test_announcement["headline"])

            # Clear form fields
            self.edit_page.clear_form()

            # Try to save empty form
            self.edit_page.save_announcement()

            # Check alert error messages (notification box)
            alert_errors = self.edit_page.get_error_messages()
            self.logger.info(f"Alert errors: {alert_errors}")

            expected_alerts = [
                Constants.VALIDATION["HEADLINE_REQUIRED"],
                Constants.VALIDATION["DESCRIPTION_REQUIRED"],
                Constants.VALIDATION["AUTHOR_REQUIRED"]
            ]
            for error in expected_alerts:
                assert error in alert_errors, f"Missing alert error: {error}"

            # Check inline field errors (under input fields)
            field_errors = self.edit_page.get_all_field_errors()
            self.logger.info(f"Field errors: {field_errors}")

            expected_fields = {
                Constants.FIELDS["HEADLINE"]["LABEL"]: Constants.INLINE_VALIDATION["HEADLINE_REQUIRED"],
                Constants.FIELDS["DESCRIPTION"]["LABEL"]: Constants.INLINE_VALIDATION["DESCRIPTION_REQUIRED"],
                Constants.FIELDS["AUTHOR"]["LABEL"]: Constants.INLINE_VALIDATION["AUTHOR_REQUIRED"]
            }

            assert field_errors == expected_fields, \
                f"Field error mismatch. Expected: {expected_fields}, Got: {field_errors}"

        except Exception as e:
            self.logger.error(f"Test failed due to exception: {str(e)}")
            raise

    def test_discard_changes_when_editing(self):
        """Test discarding changes when editing an announcement"""
        # Navigate to the announcements page and edit an existing announcement
        self.announcements_page.search_announcement(self.test_announcement["headline"])
        self.announcements_page.edit_announcement(self.test_announcement["headline"])

        # Modify announcement details
        self.edit_page.fill_announcement_form(
            headline="Edited Announcement",
            description="This should not be saved",
            content="This content should also be discarded",
            author="Test Author",
            announcement_category="KC CATEGORY",
            date=None
        )

        # Click discard
        self.edit_page.discard_changes()

        # Verify back on announcements page
        assert "/admin/announcements" in self.driver.current_url

