import importlib
import logging
import os
from typing import Dict, Any


class PluginManager:
    def __init__(self, plugin_dir: str = 'plugins'):
        self.logger = logging.getLogger(__name__)
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Any] = {}

    def load_plugins(self):
        self.logger.info(f"Loading plugins from {self.plugin_dir}")
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            self.logger.info(f"Created plugin directory: {self.plugin_dir}")

        if not os.listdir(self.plugin_dir):
            self.logger.warning(f"No plugins found in {self.plugin_dir}")
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                plugin_name = filename[:-3]
                try:
                    module = importlib.import_module(f'{self.plugin_dir}.{plugin_name}')
                    if hasattr(module, 'setup'):
                        self.plugins[plugin_name] = module.setup()
                        self.logger.info(f"Loaded plugin: {plugin_name}")
                    else:
                        self.logger.warning(f"Plugin {plugin_name} does not have a setup function")
                except Exception as e:
                    self.logger.error(f"Failed to load plugin {plugin_name}: {str(e)}")

    def get_plugin(self, name: str) -> Any:
        return self.plugins.get(name)

    def execute_plugin(self, name: str, *args, **kwargs):
        plugin = self.get_plugin(name)
        if plugin:
            try:
                return plugin.execute(*args, **kwargs)
            except Exception as e:
                self.logger.error(f"Error executing plugin {name}: {str(e)}")
        else:
            self.logger.warning(f"Plugin {name} not found")

    def list_plugins(self) -> list:
        return list(self.plugins.keys())

    def unload_plugin(self, name: str):
        if name in self.plugins:
            del self.plugins[name]
            self.logger.info(f"Unloaded plugin: {name}")
        else:
            self.logger.warning(f"Plugin {name} not found")
