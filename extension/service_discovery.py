import logging
from typing import Dict, Any
import requests

class ServiceDiscovery:
    def __init__(self, discovery_url: str):
        self.logger = logging.getLogger(__name__)
        self.discovery_url = discovery_url
        self.services: Dict[str, Any] = {}

    def discover_services(self):
        self.logger.info("Discovering services")
        try:
            response = requests.get(self.discovery_url)
            if response.status_code == 200:
                self.services = response.json()
                self.logger.info(f"Discovered {len(self.services)} services")
            else:
                self.logger.error(f"Failed to discover services. Status code: {response.status_code}")
        except requests.RequestException as e:
            self.logger.error(f"Error during service discovery: {str(e)}")

    def get_service(self, name: str) -> Dict[str, Any]:
        service = self.services.get(name)
        if service:
            return service
        else:
            self.logger.warning(f"Service {name} not found")
            return {}

    def register_service(self, name: str, url: str, metadata: Dict[str, Any] = None):
        self.logger.info(f"Registering service: {name}")
        try:
            data = {"name": name, "url": url, "metadata": metadata or {}}
            response = requests.post(f"{self.discovery_url}/register", json=data)
            if response.status_code == 200:
                self.services[name] = data
                self.logger.info(f"Service {name} registered successfully")
            else:
                self.logger.error(f"Failed to register service {name}. Status code: {response.status_code}")
        except requests.RequestException as e:
            self.logger.error(f"Error registering service {name}: {str(e)}")

    def deregister_service(self, name: str):
        self.logger.info(f"Deregistering service: {name}")
        try:
            response = requests.post(f"{self.discovery_url}/deregister", json={"name": name})
            if response.status_code == 200:
                self.services.pop(name, None)
                self.logger.info(f"Service {name} deregistered successfully")
            else:
                self.logger.error(f"Failed to deregister service {name}. Status code: {response.status_code}")
        except requests.RequestException as e:
            self.logger.error(f"Error deregistering service {name}: {str(e)}")