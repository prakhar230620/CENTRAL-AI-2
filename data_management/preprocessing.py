import logging
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class Preprocessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pipeline = None

    def create_pipeline(self, numeric_features: list[str], categorical_features: list[str]):
        self.logger.info("Creating preprocessing pipeline")
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        self.pipeline = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        self.logger.info("Preprocessing pipeline created successfully")

    def fit_transform(self, data: pd.DataFrame) -> np.ndarray:
        if self.pipeline is None:
            self.logger.error("Pipeline not created. Call create_pipeline first.")
            raise ValueError("Pipeline not created")

        self.logger.info("Fitting and transforming data")
        try:
            transformed_data = self.pipeline.fit_transform(data)
            self.logger.info(f"Data transformed successfully. Shape: {transformed_data.shape}")
            return transformed_data
        except Exception as e:
            self.logger.error(f"Error in fit_transform: {str(e)}")
            raise

    def transform(self, data: pd.DataFrame) -> np.ndarray:
        if self.pipeline is None:
            self.logger.error("Pipeline not created. Call create_pipeline first.")
            raise ValueError("Pipeline not created")

        self.logger.info("Transforming data")
        try:
            transformed_data = self.pipeline.transform(data)
            self.logger.info(f"Data transformed successfully. Shape: {transformed_data.shape}")
            return transformed_data
        except Exception as e:
            self.logger.error(f"Error in transform: {str(e)}")
            raise