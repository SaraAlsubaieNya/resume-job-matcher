import yaml
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def get(self, key_path, default=None):
        """Get nested config value using dot notation"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            value = value.get(key, {})
        return value if value != {} else default

config = Config()