from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from .base_page import BasePage

class AddCategoryPage(BasePage):
    # Header Elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header .fw-bold")
    BACK_BUTTON = (By.CSS_SELECTOR, "a[data-bs-title='Back']")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.btn.btn--success[type='submit']")
    DISCARD_BUTTON = (By.CSS_SELECTOR, "a.btn.btn--outline-danger[href='/admin/categories']")
    
    # Form Fields
    ACTIVE_SWITCH = (By.ID, "category_active")
    NAME_INPUT = (By.ID, "category_name")
    DESCRIPTION_INPUT = (By.ID, "category_description")
    SORT_ORDER_INPUT = (By.ID, "category_sort_order")
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

    def get_error_messages(self):
        """Get list of error messages from notification"""
        try:
            self.wait.until(EC.presence_of_element_located(self.ERROR_ALERT))
            errors = self.find_elements(self.ERROR_LIST)
            return [error.text for error in errors]
        except Exception as e:
            self.logger.error(f"Failed to get error messages: {str(e)}")
            return []
