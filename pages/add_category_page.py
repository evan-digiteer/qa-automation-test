from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # Add this import
import os  # Add this import
from .base_page import BasePage

class AddCategoryPage(BasePage):
    # Header Elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header .fw-bold")
    BACK_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Back']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.btn.btn--success[type='submit']")
    DISCARD_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--outline-danger[href='/admin/categories']")
    
    # Form Elements
    PHOTO_UPLOAD = (By.CSS_SELECTOR, ".js-open-gallery")
    PHOTO_PREVIEW = (By.ID, "photo-url-field-preview")
    PHOTO_FIELD = (By.ID, "photo-url-field")
    PHOTO_DIMENSIONS = (By.CSS_SELECTOR, ".text-info.overline")
    
    # Form Fields
    ACTIVE_SWITCH = (By.ID, "category_active")
    NAME_INPUT = (By.ID, "category_name")
    DESCRIPTION_INPUT = (By.ID, "category_description")
    SORT_ORDER_INPUT = (By.ID, "category_sort_order")
    
    # Validation Elements
    ERROR_CONTAINER = (By.ID, "formErrorStream")
    FIELD_ERRORS = (By.CSS_SELECTOR, ".field-helper")

    # Gallery Modal Elements
    GALLERY_WRAPPER = (By.ID, "gallery-wrapper")
    GALLERY_MODAL = (By.CLASS_NAME, "gallery-wrapper--open")
    GALLERY_UPLOAD_INPUT = (By.CSS_SELECTOR, "input.file_input[accept*='image'][type='file']")
    GALLERY_ALLOWED_TYPES = "image/png, image/jpg, image/jpeg, image/gif"
    GALLERY_UPLOAD_BUTTON = (By.CSS_SELECTOR, "#main_file_input_btn .btn--success")
    GALLERY_PHOTOS = (By.CSS_SELECTOR, ".gallery-thumbnail.gallery-photo")
    GALLERY_PHOTO_ITEM = (By.CLASS_NAME, "photo-item")
    GALLERY_SELECT_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--primary.btn--xs.insert-img")
    GALLERY_CLOSE = (By.CLASS_NAME, "close-gallery")
    UPLOAD_PROGRESS = (By.CLASS_NAME, "progress-bar-container")
    UPLOAD_STATUS = (By.CSS_SELECTOR, ".bar-wrapper .percent")
    PHOTO_PREVIEW_UPDATED = (By.CSS_SELECTOR, "#photo-url-field-preview:not([src*='placeholder'])")

    # Clean gallery locators - keep only what we need
    GALLERY_OPENER = (By.CSS_SELECTOR, ".js-open-gallery")
    GALLERY_MODAL = (By.ID, "gallery-wrapper")
    FILE_INPUT = (By.CSS_SELECTOR, "#main_file_input")
    PREVIEW_IMAGE = (By.ID, "photo-url-field-preview")
    GALLERY_PREVIEW = (By.CSS_SELECTOR, ".gallery-photo-wrapper img")
    ADD_PHOTO_BTN = (By.CSS_SELECTOR, "a.btn.btn--primary.insert-img:not(.hidden)")
    UPLOAD_BUTTON = (By.CSS_SELECTOR, ".gallery-upload-btn .btn.btn--success")
    PROGRESS_BAR = (By.CSS_SELECTOR, ".progress-bar-container")
    PROGRESS_TEXT = (By.CSS_SELECTOR, ".bar-wrapper .percent")
    NEW_PHOTO = (By.CSS_SELECTOR, ".photo-item:first-child .gallery-thumbnail")

    # Simplified gallery locators
    GALLERY_OPENER = (By.CSS_SELECTOR, ".js-open-gallery")
    GALLERY_MODAL = (By.ID, "gallery-wrapper")
    FILE_INPUT = (By.CSS_SELECTOR, "input.file_input[type='file']")  # Direct file input selector
    PREVIEW_IMAGE = (By.ID, "photo-url-field-preview")
    UPLOAD_STATUS = (By.CSS_SELECTOR, ".progress-bar-container .percent")
    PHOTO_ITEM = (By.CSS_SELECTOR, ".photo-item")
    ADD_PHOTO_BTN = (By.CSS_SELECTOR, "a.btn.btn--primary.btn--xs.insert-img[data-action='click->admin--gallery#insertPhoto']")
    GALLERY_PHOTO = (By.CSS_SELECTOR, ".gallery-thumbnail.gallery-photo")  # First existing photo

    def clear_form(self):
        """Clear all form fields with explicit waits"""
        try:
            # Clear sort order field with special handling
            sort_order_field = self.find_element(self.SORT_ORDER_INPUT)
            sort_order_field.click()  # Focus field
            sort_order_field.clear()  # Clear existing value
            # Send backspace to ensure field is empty
            sort_order_field.send_keys('\b' * 10)  
            
            # Clear other fields normally
            self.find_element(self.NAME_INPUT).clear()
            self.find_element(self.DESCRIPTION_INPUT).clear()
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear form: {str(e)}")
            return False

    def fill_category_form(self, name, description, sort_order, active=True):
        """Fill in the category form with careful sort order handling"""
        try:
            # Clear existing data first
            self.clear_form()
            
            # Set active status
            if active != self.find_element(self.ACTIVE_SWITCH).is_selected():
                self.click(self.ACTIVE_SWITCH)
            
            # Fill name and description
            self.type(self.NAME_INPUT, name)
            self.type(self.DESCRIPTION_INPUT, description)
            
            # Handle sort order field carefully
            sort_field = self.find_element(self.SORT_ORDER_INPUT)
            sort_field.click()  # Focus field
            sort_field.clear()  # Clear again to be sure
            self.driver.execute_script("arguments[0].value = '';", sort_field)  # Clear via JS
            sort_field.send_keys(str(sort_order))  # Send sort order value
            
            # Verify sort order value
            actual_value = sort_field.get_attribute('value')
            if actual_value != str(sort_order):
                self.logger.warning(f"Sort order value mismatch. Expected: {sort_order}, Got: {actual_value}")
                # Try setting value one more time
                sort_field.clear()
                sort_field.send_keys(str(sort_order))
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to fill category form: {str(e)}")
            return False

    def save_category(self):
        """Click save button and wait for response"""
        try:
            self.click(self.SAVE_BUTTON)
            # Wait for either success navigation or error message
            self.wait.until(lambda d: 
                "/admin/categories" in d.current_url or 
                self.is_element_visible(self.ERROR_CONTAINER)
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to save category: {str(e)}")
            return False

    def discard_changes(self):
        """Navigate back to categories page"""
        try:
            # Store current URL for comparison
            current_url = self.driver.current_url
            
            # Click discard button
            self.wait.until(EC.element_to_be_clickable(self.DISCARD_BUTTON)).click()
            
            # Wait for URL to change back to categories
            self.wait.until(EC.url_changes(current_url))
            self.wait.until(EC.url_contains("/admin/categories"))
            
            # Wait for categories page to load
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            
            self.logger.info("Successfully navigated back to categories page")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to navigate back: {str(e)}")
            return False

    def get_field_error(self, field_id):
        """Get error message for specific field"""
        try:
            field = self.find_element((By.ID, field_id))
            error = field.find_element(By.XPATH, "../following-sibling::div[@class='field-helper']")
            return error.text
        except:
            return None

    def verify_page_loaded(self):
        """Verify page is loaded with all required elements"""
        elements = [
            self.PAGE_TITLE,
            self.NAME_INPUT,
            self.DESCRIPTION_INPUT,
            self.SORT_ORDER_INPUT,
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
