import logging
import pandas as pd
from typing import Union, List


class DataIntake:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def ingest_data(self, source: Union[str, List[str]], data_type: str = 'csv') -> pd.DataFrame:
        self.logger.info(f"Ingesting data from {source}")
        try:
            if data_type == 'csv':
                if isinstance(source, str):
                    data = pd.read_csv(source)
                elif isinstance(source, list):
                    data = pd.concat([pd.read_csv(s) for s in source])
                else:
                    raise ValueError("Source must be a string or list of strings")
            elif data_type == 'json':
                if isinstance(source, str):
                    data = pd.read_json(source)
                elif isinstance(source, list):
                    data = pd.concat([pd.read_json(s) for s in source])
                else:
                    raise ValueError("Source must be a string or list of strings")
            else:
                raise ValueError(f"Unsupported data type: {data_type}")

            self.logger.info(f"Successfully ingested data. Shape: {data.shape}")
            return data
        except Exception as e:
            self.logger.error(f"Error ingesting data: {str(e)}")
            raise

    def validate_data(self, data: pd.DataFrame, schema: dict) -> bool:
        self.logger.info("Validating data")
        try:
            for column, dtype in schema.items():
                if column not in data.columns:
                    self.logger.error(f"Column {column} not found in data")
                    return False
                if data[column].dtype != dtype:
                    self.logger.error(
                        f"Column {column} has incorrect dtype. Expected {dtype}, got {data[column].dtype}")
                    return False
            self.logger.info("Data validation successful")
            return True
        except Exception as e:
            self.logger.error(f"Error validating data: {str(e)}")
            return False