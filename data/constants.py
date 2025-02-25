class URLs:
    LOGIN_PAGE = "/login"
    DASHBOARD = "/dashboard"
    USERS_PAGE = "/users"

class ValidationData:
    INVALID_EMAILS = [
        "plainaddress",
        "@still-invalid",
        "invalid@",
        "invalid@.com",
        "@invalid.com",
    ]
    
    INVALID_PASSWORDS = [
        "",  # Empty password
        "short",  # Too short
        "a" * 100,  # Too long
        "password123",  # Common password
        "<script>alert(1)</script>",  # XSS attempt
    ]

    USER_ROLES = [
        "Administrator"
    ]

    USER_STATUSES = {
        "ACTIVE": "Active",
        "INACTIVE": "Inactive"
    }

    USER_MESSAGES = {
        "USER_CREATED": "User was successfully created",
        "USER_UPDATED": "User was successfully updated",
        "USER_DELETED": "User was successfully deleted",
        "REQUIRED_FIELD": "This field is required",
        "INVALID_EMAIL": "Please enter a valid email address",
        "DUPLICATE_EMAIL": "Email has already been taken"
    }

    ERROR_MESSAGES = {
        "REQUIRED_FIELD": "This field is required",
        "INVALID_EMAIL": "Please enter a valid email address",
        "INVALID_PASSWORD": "Password must be between 8 and 32 characters",
        "INVALID_CREDENTIALS": "Invalid email or password"
    }

class ExpectedElements:
    LOGIN_PAGE = {
        "title": "Log In",  
        "email_placeholder": "Enter your email address",
        "password_placeholder": "Enter password",
        "login_button_text": "Log In",
        "email_label": "Email",
        "password_label": "Password",
        "heading_text": "Login",
        "forgot_password_text": "Forgot your password?",
        "email_error_text": "Invalid email address"
    }

    USERS_PAGE = {
        "title": "Users",
        "table_headers": ["Name", "Email", "Role", "Status", "Action"],
        "status_badges": {
            "active": "badge--success",
            "inactive": "badge--danger"
        }
    }

class TableColumns:
    NAME = "1"
    EMAIL = "2"
    ROLE = "3"
    STATUS = "4"

class CategoryPage:
    TITLE = "Categories"
    SORT_OPTIONS = {
        "NAME_ASC": "name asc",  # Maps to "Category Name A-Z"
        "NAME_DESC": "name desc",  # Maps to "Category Name Z-A"
        "ORDER_ASC": "sort_order asc",  # Maps to "Sort Order Ascending"
        "ORDER_DESC": "sort_order desc"  # Maps to "Sort Order Descending"
    }
    SORT_LABELS = {
        "NAME_ASC": "Category Name A-Z",
        "NAME_DESC": "Category Name Z-A",
        "ORDER_ASC": "Sort Order Ascending",
        "ORDER_DESC": "Sort Order Descending"
    }
    ITEMS_PER_PAGE_OPTIONS = [10, 25, 50]
    URLS = {
        "NEW": "/admin/categories/new",
        "LIST": "/admin/categories",
        "EDIT": "/admin/categories/{id}/edit"
    }
    STATUS = {
        "ACTIVE": "Active",
        "INACTIVE": "Inactive"
    }
    TABLE_HEADERS = ["Category Name", "Sort Order", "Status", "Action"]
    MESSAGES = {
        "CREATED": "Category was successfully created",
        "UPDATED": "Category was successfully updated",
        "DELETED": "Category was successfully deleted"
    }
