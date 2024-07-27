import logging
import pandas as pd
import json
import os
from typing import Union

class StorageManager:
    def __init__(self, base_path: str = './data'):
        self.logger = logging.getLogger(__name__)
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save_data(self, data: Union[pd.DataFrame, dict], name: str, format: str = 'csv'):
        self.logger.info(f"Saving data: {name}.{format}")
        try:
            full_path = os.path.join(self.base_path, f"{name}.{format}")
            if format == 'csv':
                data.to_csv(full_path, index=False)
            elif format == 'json':
                if isinstance(data, pd.DataFrame):
                    data.to_json(full_path, orient='records')
                elif isinstance(data, dict):
                    with open(full_path, 'w') as f:
                        json.dump(data, f)
                else:
                    raise ValueError("Data must be a DataFrame or dict for JSON format")
            else:
                raise ValueError(f"Unsupported format: {format}")
            self.logger.info(f"Data saved successfully: {full_path}")
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
            raise

    def load_data(self, name: str, format: str = 'csv') -> Union[pd.DataFrame, dict]:
        self.logger.info(f"Loading data: {name}.{format}")
        try:
            full_path = os.path.join(self.base_path, f"{name}.{format}")
            if format == 'csv':
                data = pd.read_csv(full_path)
            elif format == 'json':
                with open(full_path, 'r') as f:
                    data = json.load(f)
            else:
                raise ValueError(f"Unsupported format: {format}")
            self.logger.info(f"Data loaded successfully: {full_path}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise

    def list_data(self) -> list[str]:
        self.logger.info("Listing available data files")
        try:
            files = os.listdir(self.base_path)
            self.logger.info(f"Found {len(files)} data files")
            return files
        except Exception as e:
            self.logger.error(f"Error listing data files: {str(e)}")
            raise

    def delete_data(self, name: str, format: str = 'csv'):
        self.logger.info(f"Deleting data: {name}.{format}")
        try:
            full_path = os.path.join(self.base_path, f"{name}.{format}")
            os.remove(full_path)
            self.logger.info(f"Data deleted successfully: {full_path}")
        except Exception as e:
            self.logger.error(f"Error deleting data: {str(e)}")
            raise