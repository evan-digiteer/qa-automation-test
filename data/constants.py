class URLs:
    LOGIN_PAGE = "/login"
    DASHBOARD = "/dashboard"
    PROFILE = "/profile"

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
