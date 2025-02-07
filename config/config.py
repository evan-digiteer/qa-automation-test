import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv('BASE_URL')
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
