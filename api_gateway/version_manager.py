import logging
from packaging import version

class VersionManager:
    def __init__(self):
        self.versions = {}
        self.logger = logging.getLogger(__name__)

    def add_version(self, api_version, implementation):
        self.versions[api_version] = implementation
        self.logger.info(f"Added API version: {api_version}")

    def get_version(self, requested_version):
        compatible_version = None
        for api_version in sorted(self.versions.keys(), key=version.parse, reverse=True):
            if version.parse(requested_version) >= version.parse(api_version):
                compatible_version = api_version
                break

        if compatible_version:
            return self.versions[compatible_version]
        else:
            self.logger.warning(f"No compatible version found for {requested_version}")
            return None

    def list_versions(self):
        return list(self.versions.keys())

    def remove_version(self, api_version):
        if api_version in self.versions:
            del self.versions[api_version]
            self.logger.info(f"Removed API version: {api_version}")
        else:
            self.logger.warning(f"Version {api_version} not found")