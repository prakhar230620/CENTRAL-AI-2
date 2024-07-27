import logging
from typing import Dict, Any

class ConnectorHub:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connectors: Dict[str, Any] = {}

    def add_connector(self, name: str, connector: Any):
        self.logger.info(f"Adding connector: {name}")
        self.connectors[name] = connector

    def remove_connector(self, name: str):
        if name in self.connectors:
            self.logger.info(f"Removing connector: {name}")
            del self.connectors[name]
        else:
            self.logger.warning(f"Connector {name} not found")

    def get_connector(self, name: str) -> Any:
        if name in self.connectors:
            return self.connectors[name]
        else:
            self.logger.error(f"Connector {name} not found")
            return None

    def list_connectors(self) -> list:
        return list(self.connectors.keys())

    def execute_task(self, connector_name: str, task: str, *args, **kwargs):
        connector = self.get_connector(connector_name)
        if connector:
            self.logger.info(f"Executing task '{task}' on connector '{connector_name}'")
            return connector.execute(task, *args, **kwargs)
        else:
            self.logger.error(f"Failed to execute task. Connector '{connector_name}' not found")
            return None