class LoginPage:
    TITLE = "Mary Grace Cafe"  # Update title to match actual page title
    HEADING = "Login"
    
    URLS = {
        "LOGIN": "/admin/login",
        "FORGOT_PASSWORD": "/admin/forgot/new",
        "DASHBOARD": "/admin/dashboard"
    }
    
    PLACEHOLDERS = {
        "EMAIL": "Enter your email address",
        "PASSWORD": "Enter your password"
    }
    
    LABELS = {
        "EMAIL": "Email",
        "PASSWORD": "Password",
        "FORGOT_PASSWORD": "Forgot your password?"
    }
    
    MESSAGES = {
        "INVALID_CREDENTIALS": "Invalid Email or password.",  # Update to match exact error message
        "REQUIRED_FIELD": "This field is required",
        "INVALID_EMAIL": "Please enter a valid email address"
    }
    
    ATTRIBUTES = {
        "PASSWORD_HIDDEN": "password",
        "PASSWORD_VISIBLE": "text"
    }
    
    BUTTONS = {
        "SHOW_PASSWORD": "Show Password",
        "HIDE_PASSWORD": "Hide Password"
    }

class UsersPage:
    TITLE = "Users"
    TABLE_HEADERS = ["User Name", "Email", "Role", "Action"]
    
    SORT_OPTIONS = {
        "NAME_ASC": "name asc",
        "NAME_DESC": "name desc",
        "EMAIL_ASC": "email asc",
        "EMAIL_DESC": "email desc"
    }
    
    ROLES = {
        "ADMIN": "Administrator",
        "CCD": "CCD",
        "RECRUITMENT": "Recruitment"
    }
    
    URLS = {
        "LIST": "/admin/users",
        "NEW": "/admin/users/new",
        "EDIT": "/admin/users/{id}/edit",
        "VIEW": "/admin/users/{id}"
    }
    
    MESSAGES = {
        "CREATED": "User was successfully created",
        "UPDATED": "User was successfully updated",
        "DELETED": "User was successfully deleted",
        "DUPLICATE_EMAIL": "Email has already been taken"
    }
    
    VALIDATION = {
        "EMAIL_REQUIRED": "Email can't be blank",
        "NAME_REQUIRED": "Name can't be blank",
        "INVALID_EMAIL": "Please enter a valid email address"
    }
    
    class TableColumns:
        NAME = 1
        EMAIL = 2
        ROLE = 3
        ACTION = 4

class CategoryPage:
    TITLE = "Categories"
    TABLE_HEADERS = ["Category Name", "Sort Order", "Status", "Action"]
    
    SORT_OPTIONS = {
        "NAME_ASC": "name asc",
        "NAME_DESC": "name desc",
        "ORDER_ASC": "sort_order asc",
        "ORDER_DESC": "sort_order desc"
    }
    
    STATUS = {
        "ACTIVE": "Active",
        "INACTIVE": "Inactive"
    }
    
    URLS = {
        "LIST": "/admin/categories",
        "NEW": "/admin/categories/new",
        "EDIT": "/admin/categories/{id}/edit"
    }
    
    MESSAGES = {
        "CREATED": "Category was successfully created",
        "UPDATED": "Category was successfully updated",
        "DELETED": "Category was successfully deleted"
    }
    
    class TableColumns:
        NAME = "1"
        SORT_ORDER = "2"
        STATUS = "3"
        ACTION = "4"

class AddCategoryPage:
    TITLE = "New Category"
    PHOTO_DIMENSIONS = "Recommended Dimensions: W x H: 1440x x 285px and up"
    
    FIELDS = {
        "NAME": "Name",
        "DESCRIPTION": "Description",
        "SORT_ORDER": "Sort Order",
        "PHOTO": "Photo"
    }
    
    VALIDATION = {
        "NAME_REQUIRED": "Name can't be blank",
        "DESCRIPTION_REQUIRED": "Description can't be blank",
        "PHOTO_REQUIRED": "Photos can't be blank",
        "SORT_ORDER_REQUIRED": "Sort order can't be blank",
        "SORT_ORDER_TAKEN": "Sort order has already been taken",
        "SORT_ORDER_INVALID": "Sort order is not a number",
        "NAME_TAKEN": "Name has already been taken"
    }
    
    PHOTO = {
        "ALLOWED_TYPES": [".jpg", ".jpeg", ".png"],
        "MAX_SIZE": "2MB",
        "DIMENSIONS": {
            "WIDTH": 1440,
            "HEIGHT": 285
        }
    }

class EditCategoryPage(AddCategoryPage):
    TITLE = "Edit Category"
    
    MESSAGES = {
        "SUCCESS": "Category was successfully updated",
        "PHOTO_CHANGED": "Photo was successfully changed"
    }

class URLs:
    """Common URLs used across the application"""
    DASHBOARD = "/admin/dashboard"
    USERS = "/admin/users"
    CONTENT_BANNER = "/admin/content-and-banner"
    PRODUCTS = "/admin/products"
    STORE_BRANCHES = "/admin/store-branches"
    ANNOUNCEMENTS = "/admin/announcements"
    CAREERS = "/admin/careers"
    ROLES = "/admin/roles"
    LOGS = "/admin/audittrails"
    CATEGORIES = "/admin/categories"
    AREAS = "/admin/areas"
    ANNOUNCEMENT_CATEGORIES = "/admin/announcement-categories"
    MESSAGES = "/admin/messages"
    FUNCTION_ROOM = "/admin/function-room-inquiries"
    
    # Submenu sections
    SYSTEM_SETTINGS = {
        "CATEGORIES": "/admin/categories",
        "AREAS": "/admin/areas",
        "ANNOUNCEMENT_CATEGORIES": "/admin/announcement-categories"
    }
    
    INQUIRIES = {
        "MESSAGES": "/admin/messages",
        "FUNCTION_ROOM": "/admin/function-room-inquiries"
    }

class SideMenu:
    """Constants for the sidebar navigation menu"""
    TITLE = "Navigation Menu"
    
    # Main menu items text
    ITEMS = {
        "DASHBOARD": "Dashboard",
        "CONTENT_BANNER": "Content & Banner",
        "PRODUCT": "Product",
        "STORE_BRANCHES": "Store Branches",
        "ANNOUNCEMENTS": "News & Announcements",
        "CAREERS": "Careers",
        "ROLES": "Roles",
        "USERS": "Users",
        "LOGS": "Logs"
    }
    
    # Collapsible sections
    SECTIONS = {
        "SYSTEM_SETTINGS": "System Settings",
        "INQUIRIES": "Inquiries"
    }
    
    # Submenu items under System Settings
    SYSTEM_SETTINGS_ITEMS = {
        "CATEGORIES": "Categories",
        "AREAS": "Areas",
        "ANNOUNCEMENT_CATEGORIES": "News & Announcements Categories"
    }
    
    # Submenu items under Inquiries
    INQUIRIES_ITEMS = {
        "MESSAGES": "Messages",
        "FUNCTION_ROOM": "Function Room"
    }
    
    # URLs for each menu item (moving from URLs class)
    URLS = {
        "DASHBOARD": "/admin/dashboard",
        "CONTENT_BANNER": "/admin/content-and-banner",
        "PRODUCT": "/admin/products",
        "STORE_BRANCHES": "/admin/store-branches",
        "ANNOUNCEMENTS": "/admin/announcements",
        "CAREERS": "/admin/careers",
        "ROLES": "/admin/roles",
        "USERS": "/admin/users",
        "LOGS": "/admin/audittrails",
        "CATEGORIES": "/admin/categories",
        "AREAS": "/admin/areas",
        "ANNOUNCEMENT_CATEGORIES": "/admin/announcement-categories",
        "MESSAGES": "/admin/messages",
        "FUNCTION_ROOM": "/admin/function-room-inquiries"
    }

class AddUserPage:
    """Constants for Add User page"""
    TITLE = "New User"
    
    # Form field labels and placeholders
    FIELDS = {
        "FIRST_NAME": {
            "LABEL": "First Name",
            "PLACEHOLDER": "Enter First Name"
        },
        "MIDDLE_NAME": {
            "LABEL": "Middle Name",
            "PLACEHOLDER": "Enter Middle Name"
        },
        "LAST_NAME": {
            "LABEL": "Last Name",
            "PLACEHOLDER": "Enter Last Name"
        },
        "EMAIL": {
            "LABEL": "Email Address",
            "PLACEHOLDER": "Enter Email Address"
        },
        "ROLE": {
            "LABEL": "Role",
            "PLACEHOLDER": "Select an Option"
        }
    }
    
    # Validation messages
    VALIDATION = {
        "NAME_REQUIRED": "Name can't be blank",
        "EMAIL_REQUIRED": "Email can't be blank",
        "EMAIL_INVALID": "Please enter a valid email address",
        "EMAIL_TAKEN": "Email has already been taken",
        "PASSWORD_REQUIRED": "Password can't be blank",
        "PASSWORD_TOO_SHORT": "Password is too short (minimum is 6 characters)",
        "PASSWORD_CONFIRMATION_REQUIRED": "Password confirmation can't be blank",
        "PASSWORDS_DONT_MATCH": "Password confirmation doesn't match Password",
        "ROLE_REQUIRED": "Role can't be blank"
    }
    
    # Success messages
    MESSAGES = {
        "CREATED": "User was successfully created.",
        "UPDATED": "User was successfully updated."
    }
    
    # Available roles
    ROLES = {
        "ADMIN": "Administrator",
        "CCD": "CCD",
        "RECRUITMENT": "Recruitment"
    }
    
    # URLs
    URLS = {
        "NEW": "/admin/users/new",
        "CREATE": "/admin/users",
        "LIST": "/admin/users"
    }
    
    # Add error messages
    ERROR_MESSAGES = {
        "REQUIRED_FIELD": "This field is required",
        "INVALID_EMAIL": "Please enter a valid email address",
        "PASSWORD_MISMATCH": "Password confirmation doesn't match Password",
        "DUPLICATE_EMAIL": "Email has already been taken",
        "PASSWORD_TOO_SHORT": "Password is too short (minimum is 6 characters)"
    }
