import os
import logging
from dotenv import load_dotenv, find_dotenv

class Config:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
        env_path = find_dotenv()
        if not env_path:
            raise Exception(".env file not found")
        
        load_dotenv(env_path)
        
        # Get and validate environment variables
        self.base_url = os.getenv('BASE_URL')
        self.username = os.getenv('APP_USERNAME')  # Updated variable name
        self.password = os.getenv('APP_PASSWORD')  # Updated variable name
        
        # Log configuration
        self.logger.info(f"Base URL: {self.base_url}")
        self.logger.info(f"Username: {self.username}")
        self.logger.info("Password: ********")
        
        # Validate required variables
        if not all([self.base_url, self.username, self.password]):
            missing = []
            if not self.base_url: missing.append("BASE_URL")
            if not self.username: missing.append("APP_USERNAME")
            if not self.password: missing.append("APP_PASSWORD")
            raise Exception(f"Missing required environment variables: {', '.join(missing)}")
