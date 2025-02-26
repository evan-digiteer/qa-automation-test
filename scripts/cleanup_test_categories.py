import os
import sys
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.categories_page import CategoriesPage
from pages.side_menu import SideMenu

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('cleanup')

def cleanup_test_categories():
    logger = setup_logger()
    wait_between_actions = 1  # seconds
    
    # Load environment variables
    load_dotenv()
    base_url = os.getenv('BASE_URL')
    username = os.getenv('APP_USERNAME')
    password = os.getenv('APP_PASSWORD')
    
    if not all([base_url, username, password]):
        logger.error("Missing required environment variables")
        return
    
    # Setup WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=chrome_options)
    
    # Add locators for error alert
    PRODUCT_ERROR_ALERT = (By.CSS_SELECTOR, ".alert.alert--danger .alert__content .col")
    
    try:
        # Initialize pages
        login_page = LoginPage(driver)
        categories_page = CategoriesPage(driver)
        side_menu = SideMenu(driver)
        
        # Login
        logger.info("Logging in...")
        driver.get(f"{base_url}/login")
        login_page.login(username, password)
        
        # Add explicit wait
        wait = WebDriverWait(driver, 20)
        
        # Navigate to categories page
        logger.info("Navigating to categories...")
        side_menu.navigate_to_system_settings_item('categories')
        time.sleep(2)  # Wait for page to settle
        
        # Set maximum items per page
        categories_page.set_items_per_page(50)  # Use maximum items per page
        time.sleep(2)  # Wait for table update
        
        deleted_count = 0
        skipped_count = 0
        has_more_pages = True
        
        while has_more_pages:
            # Get fresh rows after each page load
            rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(categories_page.TABLE_ROWS)
            )
            
            if not rows:
                logger.info("No categories found on current page")
                break
                
            # Process each row index instead of the row element
            for i in range(len(rows)):
                try:
                    # Get fresh row element for each iteration
                    current_row = driver.find_elements(*categories_page.TABLE_ROWS)[i]
                    name = current_row.find_element(*categories_page.CATEGORY_NAME).text.strip()
                    
                    if 'test' in name.lower():
                        logger.info(f"Found test category: {name}")
                        
                        # Try to delete
                        if categories_page.delete_category(name):
                            try:
                                error_elem = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located(PRODUCT_ERROR_ALERT)
                                )
                                if "Cannot delete" in error_elem.text:
                                    logger.info(f"Skipping '{name}' - Cannot delete due to associations")
                                    skipped_count += 1
                                    continue
                            except:
                                deleted_count += 1
                                logger.info(f"Successfully deleted: {name}")
                                time.sleep(wait_between_actions)
                                # After deletion, get fresh rows
                                break  # Break to refresh row list
                        else:
                            logger.warning(f"Failed to delete: {name}")
                            
                except Exception as e:
                    logger.warning(f"Error processing row {i}: {str(e)}")
                    continue
                
                time.sleep(0.5)
            
            # Check for next page with explicit wait
            try:
                next_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(categories_page.NEXT_PAGE)
                )
                if "disabled" not in next_button.get_attribute("class"):
                    logger.info("Moving to next page...")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)
                else:
                    has_more_pages = False
                    logger.info("Reached last page")
            except:
                has_more_pages = False
                logger.info("No more pages found")
        
        logger.info(f"Cleanup complete. Deleted: {deleted_count}, Skipped: {skipped_count} categories")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    cleanup_test_categories()
