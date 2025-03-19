from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from .base_page import BasePage

class AddAnnouncementPage(BasePage):
    # Header Elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header .fw-bold")
    BACK_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Back']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.btn.btn--success[type='submit']")
    DISCARD_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--outline-danger[href='/admin/announcements']")

    # Form Fields
    ACTIVE_SWITCH = (By.ID, "announcement_active")
    FEATURED_SWITCH = (By.ID, "announcement_featured")
    SHOW_RIBBON_SWITCH = (By.ID, "announcement_show_ribbon")
    ANNOUNCEMENT_CATEGORY_DROPDOWN = (By.ID, "announcement_announcement_category_id-ts-control")
    HEADLINE_INPUT = (By.ID, "announcement_headline")
    DESCRIPTION_INPUT = (By.ID, "announcement_description")
    AUTHOR_INPUT = (By.ID, "announcement_author")
    DATE_INPUT = (By.CSS_SELECTOR, ".field-container input.form-control.input")
    CONTENT_INPUT = (By.CSS_SELECTOR, "div.jodit-wysiwyg")
    PHOTO_DIMENSIONS = (By.CSS_SELECTOR, ".text-info.overline")

    # Validation and Error Elements
    ERROR_CONTAINER = (By.ID, "formErrorStream")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert.alert--soft-danger")
    ERROR_LIST = (By.CSS_SELECTOR, ".alert.alert--soft-danger .alert__content ul li")
    FIELD_GROUP = (By.CLASS_NAME, "field-group")
    FIELD_ERROR = (By.CLASS_NAME, "field-helper")
    INVALID_FIELD_GROUP = (By.CLASS_NAME, "field-group--invalid")

    # Gallery Elements
    GALLERY_OPENER = (By.CSS_SELECTOR, ".js-open-gallery")
    GALLERY_MODAL = (By.ID, "gallery-wrapper")
    GALLERY_PHOTO = (By.CSS_SELECTOR, ".gallery-thumbnail.gallery-photo")
    ADD_PHOTO_BTN = (By.CSS_SELECTOR, "a.btn.btn--primary.insert-img[data-action='click->admin--gallery#insertPhoto']")
    PREVIEW_IMAGE = (By.ID, "photo-url-field-preview")

    def clear_form(self):
        """Clear all form fields with explicit waits"""
        try:
            # Uncheck switches if they are active
            for switch in [self.ACTIVE_SWITCH, self.FEATURED_SWITCH, self.SHOW_RIBBON_SWITCH]:
                switch_element = self.find_element(switch)
                if switch_element.is_selected():  # Check if switch is ON
                    switch_element.click()  # Toggle OFF

            # Reset announcement category dropdown
            dropdown = self.find_element(self.ANNOUNCEMENT_CATEGORY_DROPDOWN)
            dropdown.click()  # Open dropdown
            dropdown.send_keys(Keys.ESCAPE)  # Close it (clears selection)

            # Clear text input fields
            self.find_element(self.HEADLINE_INPUT).clear()
            self.find_element(self.DESCRIPTION_INPUT).clear()
            self.find_element(self.AUTHOR_INPUT).clear()

            # Reset date input
            date_input = self.find_element(self.DATE_INPUT)
            date_input.clear()

            # Clear content
            content_input = self.find_element(self.CONTENT_INPUT)
            content_input.clear()
            content_input.send_keys(Keys.CONTROL + "a")
            content_input.send_keys(Keys.BACKSPACE)

            return True
        except Exception as e:
            self.logger.error(f"Failed to clear form: {str(e)}")
            return False

    def fill_announcement_form(self, headline, description, author, date, announcement_category, content, active=True, featured=False, show_ribbon=False):
        """Fill in the announcement form"""
        try:
            # Clear existing data first
            self.clear_form()

            # Fill headline, description, and author
            self.type(self.HEADLINE_INPUT, headline)
            self.type(self.DESCRIPTION_INPUT, description)
            self.type(self.AUTHOR_INPUT, author)

            # Set date
            date_input = self.find_element(self.DATE_INPUT)
            date_input.click()  # Open the date picker
            self.find_element((By.CSS_SELECTOR, ".flatpickr-day.today")).click()  # Select today's date

            # Select announcement category from dropdown
            dropdown = self.find_element(self.ANNOUNCEMENT_CATEGORY_DROPDOWN)
            dropdown.click()
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "announcement_announcement_category_id-ts-dropdown"))
            )
            option_xpath = f"//div[@id='announcement_announcement_category_id-ts-dropdown']//div[contains(text(), '{announcement_category}')]"
            option = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, option_xpath))
            )
            option.click()

            # Fill content
            wysiwyg_editor = self.find_element(self.CONTENT_INPUT)
            wysiwyg_editor.send_keys(content)

            # Set switches
            switch_states = {
                self.ACTIVE_SWITCH: active,
                self.FEATURED_SWITCH: featured,
                self.SHOW_RIBBON_SWITCH: show_ribbon
            }
            for switch, state in switch_states.items():
                switch_element = self.find_element(switch)
                if switch_element.is_selected() != state:
                    switch_element.click()

            return True
        except Exception as e:
            self.logger.error(f"Failed to fill announcement form: {str(e)}")
            return False

    def save_announcement(self):
        """Click save button and wait for response"""
        try:
            self.click(self.SAVE_BUTTON)
            # Wait for either success navigation or error message
            self.wait.until(lambda d:
                "/admin/announcements" in d.current_url or
                self.is_element_visible(self.ERROR_CONTAINER)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to save announcement: {str(e)}")
            return False

    def discard_changes(self):
        """Navigate back to announcements page"""
        try:
            # Store current URL for comparison
            current_url = self.driver.current_url

            # Click discard button
            self.wait.until(EC.element_to_be_clickable(self.DISCARD_BUTTON)).click()

            # Wait for URL to change back to announcements
            self.wait.until(EC.url_changes(current_url))
            self.wait.until(EC.url_contains("/admin/announcements"))

            # Wait for announcements page to load
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

            self.logger.info("Successfully navigated back to announcements page")
            return True

        except Exception as e:
            self.logger.error(f"Failed to navigate back: {str(e)}")
            return False

    def get_field_error(self, field_id):
        """Get inline error message for a specific field"""
        try:
            # Find the field group containing the input
            field = self.find_element((By.ID, field_id))
            field_group = field.find_element(By.XPATH, "./ancestor::div[contains(@class, 'field-group')]")

            # Check if field group has invalid class
            if "field-group--invalid" in field_group.get_attribute("class"):
                error = field_group.find_element(*self.FIELD_ERROR)
                return error.text if error.is_displayed() else None

            return None

        except Exception as e:
            self.logger.error(f"Failed to get field error for {field_id}: {str(e)}")
            return None

    def get_all_field_errors(self):
        """Get all inline field error messages"""
        try:
            errors = {}
            invalid_groups = self.find_elements(self.INVALID_FIELD_GROUP)

            for group in invalid_groups:
                try:
                    label = group.find_element(By.CLASS_NAME, "label").text.strip()
                    error = group.find_element(*self.FIELD_ERROR).text.strip()
                    if error:
                        errors[label] = error
                except:
                    continue

            return errors

        except Exception as e:
            self.logger.error(f"Failed to get field errors: {str(e)}")
            return {}

    def verify_page_loaded(self):
        """Verify page is loaded with all required elements"""
        elements = [
            self.PAGE_TITLE,
            self.HEADLINE_INPUT,
            self.DESCRIPTION_INPUT,
            self.AUTHOR_INPUT,
            self.DATE_INPUT,
            self.CONTENT_INPUT,
            self.SAVE_BUTTON,
            self.DISCARD_BUTTON
        ]

        try:
            for element in elements:
                assert self.is_element_visible(element), f"Element not visible: {element}"
            return True
        except Exception as e:
            self.logger.error(f"Page verification failed: {str(e)}")
            return False

    def upload_photo(self, file_path=None):
        """Select an existing photo from gallery"""
        try:
            self.logger.info("Opening gallery to select photo")

            # Open gallery
            self.wait.until(EC.element_to_be_clickable(self.GALLERY_OPENER)).click()
            self.logger.info("Gallery opened")

            # Wait for modal and first photo
            self.wait.until(EC.presence_of_element_located(self.GALLERY_MODAL))
            photo = self.wait.until(EC.element_to_be_clickable(self.GALLERY_PHOTO))

            # Click the first available photo
            photo.click()
            self.logger.info("Photo selected")

            # Click Add Selected Photo button
            add_btn = self.wait.until(EC.element_to_be_clickable(self.ADD_PHOTO_BTN))
            add_btn.click()
            self.logger.info("Add photo clicked")

            # Verify preview updated
            self.wait.until(
                lambda d: 'placeholder' not in
                          d.find_element(*self.PREVIEW_IMAGE).get_attribute('src')
            )
            self.logger.info("Preview updated")

            return True

        except Exception as e:
            self.logger.error(f"Photo selection failed: {str(e)}")
            self.logger.error(f"Current URL: {self.driver.current_url}")
            return False

    def get_error_messages(self):
        """Get list of error messages from notification"""
        try:
            self.wait.until(EC.presence_of_element_located(self.ERROR_ALERT))
            errors = self.find_elements(self.ERROR_LIST)
            return [error.text for error in errors]
        except Exception as e:
            self.logger.error(f"Failed to get error messages: {str(e)}")
            return []