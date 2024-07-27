import logging
from typing import Dict, Any

class ModelRegistry:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models: Dict[str, Any] = {}

    def register_model(self, name: str, model: Any):
        self.logger.info(f"Registering model: {name}")
        self.models[name] = model

    def unregister_model(self, name: str):
        if name in self.models:
            self.logger.info(f"Unregistering model: {name}")
            del self.models[name]
        else:
            self.logger.warning(f"Model {name} not found")

    def get_model(self, name: str) -> Any:
        if name in self.models:
            return self.models[name]
        else:
            self.logger.error(f"Model {name} not found")
            return None

    def list_models(self) -> list:
        return list(self.models.keys())

    def update_model(self, name: str, updated_model: Any):
        if name in self.models:
            self.logger.info(f"Updating model: {name}")
            self.models[name] = updated_model
        else:
            self.logger.warning(f"Model {name} not found. Cannot update.")