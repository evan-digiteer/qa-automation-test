import pytest
import logging
import os
from datetime import datetime
from utils.webdriver_factory import WebDriverFactory
from config.config import Config

def create_screenshot_dirs():
    """Create screenshots directory structure"""
    base_dir = "screenshots"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    date_dir = os.path.join(base_dir, datetime.now().strftime('%Y-%m-%d'))
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    return date_dir

def take_screenshot(driver, name):
    """Take screenshot and save it in organized directory structure"""
    timestamp = datetime.now().strftime('%H-%M-%S')
    screenshot_dir = create_screenshot_dirs()
    clean_name = "".join(char for char in name if char.isalnum() or char in (' ', '-', '_')).rstrip()
    screenshot_path = os.path.join(screenshot_dir, f"{clean_name}_{timestamp}.png")
    
    try:
        driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logging.error(f"Failed to save screenshot: {str(e)}")

@pytest.fixture(scope="session")
def config():
    return Config()

@pytest.fixture(scope="function")
def driver(request):
    driver = WebDriverFactory.get_driver()
    driver.maximize_window()
    
    def teardown():
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            take_screenshot(driver, request.node.name)
        driver.quit()
    
    request.addfinalizer(teardown)
    return driver

def pytest_configure(config):
    """Configure test session - runs before any tests"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_name = f"report_{timestamp}.html"
    
    # Create reports directory if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    # Set the HTML report path
    config.option.htmlpath = os.path.join("reports", report_name)
    print(f"\nHTML report will be generated at: {config.option.htmlpath}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
