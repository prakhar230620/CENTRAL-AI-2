import logging
from typing import Dict, Any
import json
from pathlib import Path

class ConfigUpdater:
    def __init__(self, config_file: str = 'config.json'):
        self.logger = logging.getLogger(__name__)
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        self.logger.info(f"Loading configuration from {self.config_file}")
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            self.logger.warning(f"Config file {self.config_file} not found. Using empty configuration.")
            return {}

    def save_config(self):
        self.logger.info(f"Saving configuration to {self.config_file}")
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def update_config(self, new_config: Dict[str, Any]):
        self.logger.info("Updating configuration")
        self.config.update(new_config)
        self.save_config()
        self.logger.info("Configuration updated successfully")

    def get_config(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set_config(self, key: str, value: Any):
        self.config[key] = value
        self.save_config()

    def delete_config(self, key: str):
        if key in self.config:
            del self.config[key]
            self.save_config()
            self.logger.info(f"Deleted configuration key: {key}")
        else:
            self.logger.warning(f"Configuration key {key} not found")

    def reset_config(self):
        self.logger.warning("Resetting configuration to default")
        self.config = {}
        self.save_config()