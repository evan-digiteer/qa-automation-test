import pytest
import logging
from datetime import datetime
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.webdriver_factory import WebDriverFactory
from config.config import Config

@pytest.fixture(scope="session")
def config():
    return Config()

@pytest.fixture(scope="function")
def driver(request):
    driver = WebDriverFactory.get_driver()
    driver.maximize_window()
    
    def teardown():
        if request.node.rep_call.failed:
            take_screenshot(driver, request.node.name)
        driver.quit()
    
    request.addfinalizer(teardown)
    return driver

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def take_screenshot(driver, name):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    screenshot_path = f"screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
