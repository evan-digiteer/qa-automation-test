from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .add_announcement_page import AddAnnouncementPage

class EditAnnouncementPage(AddAnnouncementPage):
    # Override title and header elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header .fw-bold")
    EDIT_TITLE_TEXT = "Edit Announcement"

    # Edit-specific elements
    CURRENT_PHOTO = (By.CSS_SELECTOR, "#photo-url-field-preview[src*='cloudfront']")
    CHANGE_PHOTO_BUTTON = (By.CSS_SELECTOR, ".change-photo-wrapper--hover")
    PHOTO_URL_FIELD = (By.ID, "photo-url-field")

    # Add gallery close button locator
    GALLERY_CLOSE_BUTTON = (By.CLASS_NAME, "close-gallery")

    # Add gallery state handling
    GALLERY_BODY = (By.CLASS_NAME, "gallery-body")
    GALLERY_OVERLAY = (By.CSS_SELECTOR, ".gallery-wrapper--open")

    def verify_existing_data(self, expected_data):
        """Verify form is populated with expected data"""
        try:

            self.logger.info("Verifying existing announcement data")

            # Wait for page to fully load first
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            self.wait.until(EC.presence_of_element_located(self.HEADLINE_INPUT))

            # Additional wait for form data to populate
            self.driver.implicitly_wait(2)

            # Get current values
            actual_data = {
                "headline": self.find_element(self.HEADLINE_INPUT).get_attribute("value"),
                "description": self.find_element(self.DESCRIPTION_INPUT).get_attribute("value"),
                "content": self.find_element(self.CONTENT_INPUT).text.strip(),
                "author": self.find_element(self.AUTHOR_INPUT).get_attribute("value"),
                "announcement_category": self.find_element(self.ANNOUNCEMENT_CATEGORY_DROPDOWN).text.strip(),
                "date": self.find_element(self.DATE_INPUT).get_attribute("value"),
                "active": self.find_element(self.ACTIVE_SWITCH).is_selected(),
                "featured": self.find_element(self.FEATURED_SWITCH).is_selected(),
                "show_ribbon": self.find_element(self.SHOW_RIBBON_SWITCH).is_selected()
            }

            # Log values for debugging
            self.logger.info(f"Actual data: {actual_data}")
            self.logger.info(f"Expected data: {expected_data}")

            # Verify each field
            for key in ["headline", "description", "content", "author", "announcement_category", "date"]:
                assert str(actual_data.get(key)) == str(expected_data.get(key)), \
                    f"{key} mismatch. Expected: {expected_data.get(key)}, Got: {actual_data.get(key)}"
            assert actual_data["active"] == expected_data["active"], \
                f"Active status mismatch. Expected: {expected_data['active']}, Got: {actual_data['active']}"

            return True

        except Exception as e:
            self.logger.error(f"Failed to verify existing data: {str(e)}")
            return False

    def wait_for_page_load(self):
        """Wait for edit page to fully load"""
        try:
            self.wait.until(EC.presence_of_element_located(self.HEADLINE_INPUT))
            self.wait.until(EC.presence_of_element_located(self.DESCRIPTION_INPUT))
            self.wait.until(EC.presence_of_element_located(self.CONTENT_INPUT))
            self.wait.until(EC.presence_of_element_located(self.AUTHOR_INPUT))
            self.wait.until(EC.presence_of_element_located(self.ANNOUNCEMENT_CATEGORY_DROPDOWN))
            self.wait.until(EC.presence_of_element_located(self.DATE_INPUT))
            self.driver.implicitly_wait(2)  # Additional wait for data population
            return True
        except Exception as e:
            self.logger.error(f"Page failed to load: {str(e)}")
            return False

    def close_gallery(self):
        """Close gallery modal if open"""
        try:
            if self.is_element_visible(self.GALLERY_OVERLAY):
                self.click(self.GALLERY_CLOSE_BUTTON)
                self.wait.until_not(EC.presence_of_element_located(self.GALLERY_OVERLAY))
                # Additional wait for animation
                self.driver.implicitly_wait(1)
            return True
        except Exception as e:
            self.logger.error(f"Failed to close gallery: {str(e)}")
            return False

    def wait_for_gallery_ready(self):
        """Wait for gallery to be in a clickable state"""
        try:
            # Wait for any existing gallery body to be gone
            self.wait.until_not(EC.presence_of_element_located(self.GALLERY_BODY))
            # Wait for any existing overlay to be gone
            self.wait.until_not(EC.presence_of_element_located(self.GALLERY_OVERLAY))
            return True
        except Exception as e:
            self.logger.error(f"Gallery not ready: {str(e)}")
            return False

    def change_photo(self):
        """Change photo using gallery with proper state handling"""
        try:
            # Ensure gallery is in clean state
            self.close_gallery()
            self.wait_for_gallery_ready()

            # Click using JavaScript to avoid intercepted click
            opener = self.wait.until(EC.presence_of_element_located(self.GALLERY_OPENER))
            self.driver.execute_script("arguments[0].click();", opener)

            # Wait for gallery to open and select photo
            result = self.upload_photo()

            # Ensure gallery is closed after upload
            self.close_gallery()
            self.wait_for_gallery_ready()

            return result

        except Exception as e:
            self.logger.error(f"Failed to change photo: {str(e)}")
            self.close_gallery()  # Try to close gallery even if error
            return False