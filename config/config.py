import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Base URL for the application
        self.base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        
        # Login credentials - Use LOGIN_EMAIL instead of USERNAME
        self.username = os.getenv('LOGIN_EMAIL')
        self.password = os.getenv('LOGIN_PASSWORD')
        
        if not all([self.username, self.password]):
            raise ValueError("Missing required environment variables LOGIN_EMAIL and LOGIN_PASSWORD")
        
        # Browser configuration
        self.browser = os.getenv('BROWSER', 'chrome')
        self.headless = os.getenv('HEADLESS', 'false').lower() == 'true'
        
        # Timeouts
        self.implicit_wait = int(os.getenv('IMPLICIT_WAIT', '10'))
        self.explicit_wait = int(os.getenv('EXPLICIT_WAIT', '20'))
        
        print("Configuration loaded successfully")
