# QA Automation Framework

Web application test automation framework using Python, Selenium, and Pytest.

## Features

- Modern page object model implementation
- Data-driven testing capabilities
- Automated screenshot capture on failures
- HTML test reporting
- Environment configuration
- Comprehensive logging system
- Test data generation
- Modular test structure

## Project Structure

```
qa-automation-test/
├── config/
│   └── config.py         # Configuration management
├── data/
│   └── constants.py      # Test data and constants
├── pages/
│   ├── base_page.py      # Base page object
│   ├── login_page.py     # Login functionality
│   ├── users_page.py     # User management
│   ├── add_user_page.py  # User creation
│   └── edit_user_page.py # User editing
├── tests/
│   ├── conftest.py       # Pytest configuration
│   ├── test_login.py     # Authentication tests
│   ├── test_add_user.py  # Creation tests
│   └── test_edit_user.py # Edit tests
├── utils/
│   └── webdriver_factory.py  # WebDriver management
├── .env                  # Environment variables
├── pytest.ini           # Pytest settings
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## Setup

1. Install Python 3.8 or higher
2. Install/Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```
   See [pip installation guide](https://pypi.org/project/pip/)

3. Install dependencies either via:
   ```bash
   pip install -r requirements.txt
   ```
   Or install packages individually:
   - [pip](https://pypi.org/project/pip/) (Latest version)
   - [selenium](https://pypi.org/project/selenium/) (v4.11.2)
   - [pytest](https://pypi.org/project/pytest/) (v7.4.0)
   - [pytest-html](https://pypi.org/project/pytest-html/) (v3.2.0)
   - [python-dotenv](https://pypi.org/project/python-dotenv/) (v1.0.0)
   - [webdriver-manager](https://pypi.org/project/webdriver-manager/) (v4.0.0)
   - [Faker](https://pypi.org/project/Faker/) (v19.13.0)

4. Configure environment variables in `.env`:
   ```
   BASE_URL=<application-url>
   APP_USERNAME=<username>
   APP_PASSWORD=<password>
   ```

## Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_login.py
pytest tests/test_add_user.py
pytest tests/test_edit_user.py
```

Run tests with HTML report:
```bash
pytest --html=report.html
```

## Test Features

### Authentication Tests
- Login success/failure scenarios
- Field validations
- Error message verification
- Page element verification

### User Management Tests
- User creation
- User editing
- Form validations
- Role management
- Duplicate detection
- Required field validation

### Framework Features
- Failure screenshots
- HTML reporting
- Console/file logging
- Page Object Model
- Data driven testing
- Dynamic test data generation
- Environment management

## Reports and Logs

- HTML reports in `/reports`
- Failure screenshots in `/screenshots`
- Console and report logging