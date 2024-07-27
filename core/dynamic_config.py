import json
import logging
from pathlib import Path

class DynamicConfig:
    def __init__(self, config_file='config.json'):
        self.logger = logging.getLogger(__name__)
        self.config_file = Path(config_file)
        self.config = {}

    def load_config(self):
        self.logger.info(f"Loading configuration from {self.config_file}")
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.logger.warning(f"Config file {self.config_file} not found. Using default configuration.")
            self.config = self.get_default_config()
        self.logger.info("Configuration loaded successfully")

    def save_config(self):
        self.logger.info(f"Saving configuration to {self.config_file}")
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
        self.logger.info("Configuration saved successfully")

    def update_config(self, new_config):
        self.logger.info("Updating configuration")
        self.config.update(new_config)
        self.save_config()

    def get_config(self, key, default=None):
        return self.config.get(key, default)

    def set_config(self, key, value):
        self.config[key] = value
        self.save_config()

    @staticmethod
    def get_default_config():
        return {
            "log_level": "INFO",
            "max_tasks": 10,
            "default_ai_model": "gpt-3.5-turbo",
            "api_rate_limit": 100
        }