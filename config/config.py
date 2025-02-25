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
        
        # Get environment variables
        self.base_url = os.getenv('BASE_URL')
        self.username = os.getenv('APP_USERNAME')
        self.password = os.getenv('APP_PASSWORD')
        
        # Validate required variables
        missing = []
        if not self.base_url: missing.append("BASE_URL")
        if not self.username: missing.append("APP_USERNAME")
        if not self.password: missing.append("APP_PASSWORD")
        
        if missing:
            raise Exception(f"Missing required environment variables: {', '.join(missing)}")
        
        # Single log message for successful configuration
        self.logger.info("Configuration loaded successfully")
