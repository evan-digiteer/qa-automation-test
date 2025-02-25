import pytest
import logging
import os
from datetime import datetime
from pathlib import Path
from string import Template
from utils.webdriver_factory import WebDriverFactory
from utils.report_utils import ReportGenerator, TestCaseLogHandler
from config.config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize report generator
report_generator = ReportGenerator()

def setup_logger():
    """Configure minimal logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',  # Simplified format
        force=True
    )
    
    # Silence verbose loggers
    logging.getLogger('WDM').setLevel(logging.ERROR)
    logging.getLogger('selenium').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('report').setLevel(logging.INFO)

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
        return screenshot_path
    except Exception as e:
        logging.error(f"Failed to save screenshot: {str(e)}")
        return None

@pytest.fixture(scope="session", autouse=True)
def setup_session():
    setup_logger()
    pytest.test_data = {}  # Single data store

@pytest.fixture(scope="session")
def config():
    return Config()

@pytest.fixture(scope="function", autouse=True)
def test_logging(request):
    """Per-test logging setup"""
    logger = logging.getLogger()
    log_handler = TestCaseLogHandler()
    logger.addHandler(log_handler)
    
    yield
    
    # Initialize test data if not exists
    if request.node.nodeid not in pytest.test_data:
        pytest.test_data[request.node.nodeid] = {}
    
    # Store logs
    pytest.test_data[request.node.nodeid]['logs'] = log_handler.get_logs()
    logger.removeHandler(log_handler)

@pytest.fixture(scope="function")
def driver(request):
    """Browser fixture with screenshot capture"""
    # Create driver using factory
    driver = WebDriverFactory.create_driver()
    
    yield driver
    
    try:
        # Take screenshot at test end
        screenshot_path = take_screenshot(driver, request.node.name)
        if request.node.nodeid not in pytest.test_data:
            pytest.test_data[request.node.nodeid] = {}
        pytest.test_data[request.node.nodeid]['screenshot'] = screenshot_path
        
    except Exception as e:
        logging.error(f"Screenshot failed for {request.node.name}: {str(e)}")
    finally:
        driver.quit()

def pytest_configure(config):
    config._metadata = None  # Clear default metadata
    pytest.screenshot_data = {}

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # Initialize test data if not exists
        if item.nodeid not in pytest.test_data:
            pytest.test_data[item.nodeid] = {}
        
        # Get error message if test failed
        error_message = None
        if call.excinfo:
            if hasattr(call.excinfo.value, 'msg'):
                error_message = str(call.excinfo.value.msg)
            else:
                error_message = str(call.excinfo.value)
        
        # Store test information
        pytest.test_data[item.nodeid].update({
            'name': item.name,
            'status': report.outcome,
            'duration': report.duration,
            'error': error_message
        })
        
        # Get the logs from our custom handler
        logs = pytest.test_data[item.nodeid].get('logs', '')
        
        # Use existing screenshot from driver fixture
        screenshot_path = pytest.test_data[item.nodeid].get('screenshot')
            
        # Create test case HTML
        html_content = report_generator.create_test_case_html(
            name=item.name,
            status=report.outcome,
            duration=report.duration,
            error=error_message,
            screenshot_path=screenshot_path,
            logs=logs
        )
        
        # Store the HTML content
        if not hasattr(item.session, 'test_results'):
            item.session.test_results = []
        item.session.test_results.append(html_content)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    try:
        logging.info("Generating HTML report")
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'report_template.html')
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        test_cases_html = []
        for nodeid, data in pytest.test_data.items():
            test_case_html = report_generator.create_test_case_html(
                name=data['name'],  # Use stored name
                status=data['status'],  # Use stored status
                duration=data['duration'],
                error=data.get('error'),
                screenshot_path=data.get('screenshot'),
                logs=data.get('logs', '')
            )
            test_cases_html.append(test_case_html)
            
            # Minimal logging
            logging.debug(f"Processed test {data['name']}")
        
        # Prepare report data
        report_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'passed': len([x for x in pytest.test_data.values() if x.get('status') == 'passed']),
            'failed': len([x for x in pytest.test_data.values() if x.get('status') == 'failed']),
            'skipped': len([x for x in pytest.test_data.values() if x.get('status') == 'skipped']),
            'duration': f"{sum(x.get('duration', 0) for x in pytest.test_data.values()):.2f}s",
            'test_cases': '\n'.join(test_cases_html)
        }
        
        # Generate report using safe substitution
        html_report = template.safe_substitute(report_data)
        
        # Save the report
        report_dir = "reports"
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        
        report_path = os.path.join(report_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        logging.info(f"HTML report generated: {report_path}")
        
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}", exc_info=True)
        raise
