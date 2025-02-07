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
        "title": "Login",
        "email_placeholder": "Enter your email address",
        "password_placeholder": "Enter password",
        "login_button_text": "Sign In"
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
