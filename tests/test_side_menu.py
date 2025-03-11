import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.side_menu import SideMenu
from pages.login_page import LoginPage
from data.constants import LoginPage as LoginConstants  # Update this import
from data.constants import SideMenu as Constants  # Update this import

class TestSideMenu:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.side_menu = SideMenu(driver)
        self.login_page = LoginPage(driver)
        self.driver = driver
        self.config = config
        
        # Login first - Update to use LoginConstants
        login_url = self.config.base_url + LoginConstants.URLS['LOGIN']
        self.driver.get(login_url)
        self.login_page.login(self.config.username, self.config.password)

    def test_sidebar_basic_elements(self):
        """Test that basic sidebar elements are present"""
        # Wait for page load
        self.driver.implicitly_wait(2)
        # Test main menu visibility using constants
        menu_items = {
            Constants.ITEMS['DASHBOARD']: self.side_menu.DASHBOARD_LINK,
            Constants.ITEMS['CONTENT_BANNER']: self.side_menu.CONTENT_BANNER_LINK,
            Constants.ITEMS['PRODUCT']: self.side_menu.PRODUCT_LINK,
            Constants.ITEMS['USERS']: self.side_menu.USERS_LINK
        }
        
        for name, locator in menu_items.items():
            assert self.side_menu.find_element(locator).is_displayed(), \
                f"{name} link not visible"

    @pytest.mark.parametrize("section,expected_url", [
        ('dashboard', Constants.URLS['DASHBOARD']),
        ('content', Constants.URLS['CONTENT_BANNER']),
        ('product', Constants.URLS['PRODUCT']),
        ('store_branches', Constants.URLS['STORE_BRANCHES']),
        ('announcements', Constants.URLS['ANNOUNCEMENTS']),
        ('careers', Constants.URLS['CAREERS']),
        ('roles', Constants.URLS['ROLES']),
        ('users', Constants.URLS['USERS']),
        ('logs', Constants.URLS['LOGS'])
    ])
    def test_main_navigation_links(self, section, expected_url):
        """Test main navigation links in sidebar"""
        # Navigate to section
        self.side_menu.navigate_to_section(section)
        # Verify URL changed correctly
        self.side_menu.wait.until(EC.url_contains(expected_url))
        assert expected_url in self.driver.current_url, f"Failed to navigate to {section}"

    def test_system_settings_expansion(self):
        """Test System Settings submenu expansion"""
        self.side_menu.expand_system_settings()
        # Verify submenu items are visible after expansion
        submenu = self.side_menu.find_element(self.side_menu.SYSTEM_SETTINGS_SECTION)
        assert 'show' in submenu.get_attribute('class'), "System Settings menu not expanded"

    def test_inquiries_expansion(self):
        """Test Inquiries submenu expansion"""
        self.side_menu.expand_inquiries()
        # Verify submenu items are visible after expansion
        submenu = self.side_menu.find_element(self.side_menu.INQUIRIES_SECTION)
        assert 'show' in submenu.get_attribute('class'), "Inquiries menu not expanded"

    def verify_navigation(self, section):
        """Helper method to verify navigation was successful"""
        section_url_mapping = {
            'dashboard': '/admin/dashboard',
            'content': '/admin/content-and-banner',
            'product': '/admin/products',
            'store_branches': '/admin/store-branches',
            'announcements': '/admin/announcements',
            'careers': '/admin/careers',
            'roles': '/admin/roles',
            'users': '/admin/users',
            'logs': '/admin/audittrails'
        }
        
        expected_url = section_url_mapping.get(section)
        if not expected_url:
            raise ValueError(f"No URL mapping found for section: {section}")

        # Wait for URL to change
        try:
            self.side_menu.wait.until(
                EC.url_contains(expected_url)
            )
            current_url = self.driver.current_url.lower()
            expected_url = expected_url.lower()
            
            self.side_menu.logger.info(f"Navigating to {section}")
            self.side_menu.logger.info(f"Current URL: {current_url}")
            self.side_menu.logger.info(f"Expected URL contains: {expected_url}")
            
            return expected_url in current_url
        except Exception as e:
            self.side_menu.logger.error(f"Navigation failed for {section}: {str(e)}")
            return False

    @pytest.mark.parametrize("section,expected_text", [
        ('dashboard', "Dashboard"),
        ('content', "Content & Banner"),
        ('product', "Product"),
        ('store_branches', "Store Branches"),
        ('announcements', "News & Announcements"),
        ('careers', "Careers"),
        ('roles', "Roles"),
        ('users', "Users"),
        ('logs', "Logs")
    ])
    def test_main_navigation_links(self, section, expected_text):
        """Test main navigation links in sidebar"""
        # Map section names to actual attribute names
        section_mapping = {
            'dashboard': 'DASHBOARD_LINK',
            'content': 'CONTENT_BANNER_LINK',
            'product': 'PRODUCT_LINK',
            'store_branches': 'STORE_BRANCHES_LINK',
            'announcements': 'ANNOUNCEMENTS_LINK',
            'careers': 'CAREERS_LINK',
            'roles': 'ROLES_LINK',
            'users': 'USERS_LINK',
            'logs': 'LOGS_LINK'
        }
        
        # Get correct attribute name
        attr_name = section_mapping.get(section)
        if not attr_name:
            pytest.fail(f"Unknown section: {section}")
            
        # Find and verify link
        link = self.side_menu.find_element(getattr(self.side_menu, attr_name))
        assert expected_text in link.text, f"Wrong text for {section} link"
        # Try navigation
        assert self.side_menu.navigate_to_section(section), f"Failed to navigate to {section}"

    def test_system_settings_expansion(self):
        """Test System Settings submenu expansion"""
        # First ensure submenu is collapsed
        self.side_menu.click(self.side_menu.SYSTEM_SETTINGS_BUTTON)
        # Wait for animation
        self.driver.implicitly_wait(1)
        # Verify expansion
        submenu = self.side_menu.find_element(self.side_menu.SYSTEM_SETTINGS_SECTION)
        assert self.side_menu.wait.until(
            lambda _: 'show' in submenu.get_attribute('class')
        ), "System Settings menu not expanded"

    def test_inquiries_expansion(self):
        """Test Inquiries submenu expansion"""
        self.side_menu.expand_inquiries()
        assert self.side_menu.is_submenu_expanded('inquiries'), \
            "Inquiries submenu did not expand"

    @pytest.mark.parametrize("item", [
        'categories',
        'areas',
        'announcement_categories'
    ])
    def test_system_settings_navigation(self, item):
        """Test navigation to System Settings submenu items"""
        assert self.side_menu.navigate_to_system_settings_item(item), \
            f"Failed to navigate to system settings item {item}"

    @pytest.mark.parametrize("item", [
        'messages',
        'function_room'
    ])
    def test_inquiries_navigation(self, item):
        """Test navigation to Inquiries submenu items"""
        self.side_menu.navigate_to_inquiries_item(item)
        current_url = self.driver.current_url
        assert item.replace('_', '-') in current_url, \
            f"Navigation failed for inquiries item {item}"

    def test_sidebar_close_button(self):
        """Test sidebar close button functionality"""
        self.side_menu.click_close_button()
        # Add appropriate assertion based on how sidebar closing is implemented
        # For example, checking for a collapsed class or style attribute
