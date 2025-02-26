from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .add_category_page import AddCategoryPage  # Inherit from AddCategoryPage since most elements are same

class EditCategoryPage(AddCategoryPage):
    # Override title and header elements
    PAGE_TITLE = (By.CSS_SELECTOR, ".card__header .fw-bold")
    EDIT_TITLE_TEXT = "Edit Category"
    
    # Edit-specific elements
    CURRENT_PHOTO = (By.CSS_SELECTOR, "#photo-url-field-preview[src*='cloudfront']")
    CHANGE_PHOTO_BUTTON = (By.CSS_SELECTOR, ".change-photo-wrapper--hover")
    PHOTO_URL_FIELD = (By.ID, "photo-url-field")
    
    # Add gallery close button locator
    GALLERY_CLOSE_BUTTON = (By.CLASS_NAME, "close-gallery")

    def verify_existing_data(self, expected_data):
        """Verify form is populated with expected data"""
        try:
            self.logger.info("Verifying existing category data")
            
            # Get current values
            actual_data = {
                "name": self.find_element(self.NAME_INPUT).get_attribute("value"),
                "description": self.find_element(self.DESCRIPTION_INPUT).get_attribute("value"),
                "sort_order": self.find_element(self.SORT_ORDER_INPUT).get_attribute("value"),
                "active": self.find_element(self.ACTIVE_SWITCH).is_selected(),
                "has_photo": self.is_element_visible(self.CURRENT_PHOTO)
            }
            
            # Verify each field
            assert actual_data["name"] == expected_data["name"], \
                f"Name mismatch. Expected: {expected_data['name']}, Got: {actual_data['name']}"
            assert actual_data["description"] == expected_data["description"], \
                f"Description mismatch. Expected: {expected_data['description']}, Got: {actual_data['description']}"
            assert str(actual_data["sort_order"]) == str(expected_data["sort_order"]), \
                f"Sort order mismatch. Expected: {expected_data['sort_order']}, Got: {actual_data['sort_order']}"
            assert actual_data["active"] == expected_data["active"], \
                f"Active status mismatch. Expected: {expected_data['active']}, Got: {actual_data['active']}"
            assert actual_data["has_photo"], "Photo not loaded"
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to verify existing data: {str(e)}")
            return False

    def close_gallery(self):
        """Close gallery modal if open"""
        try:
            if self.is_element_visible(self.GALLERY_MODAL):
                self.click(self.GALLERY_CLOSE_BUTTON)
                self.wait.until_not(EC.visibility_of_element_located(self.GALLERY_MODAL))
            return True
        except Exception as e:
            self.logger.error(f"Failed to close gallery: {str(e)}")
            return False

    def change_photo(self):
        """Change photo using gallery with proper cleanup"""
        try:
            # Close gallery if already open
            self.close_gallery()
            
            # Now try to open and change photo
            self.click(self.CHANGE_PHOTO_BUTTON)
            result = self.upload_photo()  # Reuse photo upload from parent
            
            # Ensure gallery is closed after upload
            self.close_gallery()
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to change photo: {str(e)}")
            self.close_gallery()  # Try to close gallery even if error
            return False
