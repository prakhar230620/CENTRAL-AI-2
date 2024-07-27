import logging
from collections import defaultdict
import random


class LoadBalancer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.services = defaultdict(list)
        self.weights = defaultdict(dict)

    def register_service(self, service_type, service_instance, weight=1):
        self.services[service_type].append(service_instance)
        self.weights[service_type][service_instance] = weight
        self.logger.info(f"Registered service: {service_type} with weight {weight}")

    def unregister_service(self, service_type, service_instance):
        if service_instance in self.services[service_type]:
            self.services[service_type].remove(service_instance)
            del self.weights[service_type][service_instance]
            self.logger.info(f"Unregistered service: {service_type}")

    def get_service(self, service_type):
        if service_type not in self.services or not self.services[service_type]:
            raise ValueError(f"No services available for type: {service_type}")

        total_weight = sum(self.weights[service_type].values())
        r = random.uniform(0, total_weight)
        upto = 0
        for service, weight in self.weights[service_type].items():
            if upto + weight >= r:
                self.logger.info(f"Selected service for type {service_type}")
                return service
            upto += weight

        # Fallback to random selection if weighted selection fails
        return random.choice(self.services[service_type])

    def get_service_count(self, service_type):
        return len(self.services[service_type])

    def get_all_service_types(self):
        return list(self.services.keys())