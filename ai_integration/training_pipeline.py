import logging
from typing import Any, Dict


class TrainingPipeline:
    def __init__(self, model_registry):
        self.logger = logging.getLogger(__name__)
        self.model_registry = model_registry
        self.training_configs: Dict[str, Dict[str, Any]] = {}

    def add_training_config(self, model_name: str, config: Dict[str, Any]):
        self.logger.info(f"Adding training config for model: {model_name}")
        self.training_configs[model_name] = config

    def remove_training_config(self, model_name: str):
        if model_name in self.training_configs:
            self.logger.info(f"Removing training config for model: {model_name}")
            del self.training_configs[model_name]
        else:
            self.logger.warning(f"Training config for model {model_name} not found")

    def train_model(self, model_name: str, dataset: Any):
        if model_name not in self.training_configs:
            self.logger.error(f"No training config found for model: {model_name}")
            return False

        model = self.model_registry.get_model(model_name)
        if not model:
            self.logger.error(f"Model {model_name} not found in registry")
            return False

        config = self.training_configs[model_name]
        self.logger.info(f"Starting training for model: {model_name}")

        try:
            # Simulating training process
            self.logger.info(f"Training model {model_name} with config: {config}")
            self.logger.info(f"Dataset size: {len(dataset)}")
            # Here you would actually train the model using the dataset and config
            # For simulation, we're just logging the process
            self.logger.info(f"Training completed for model: {model_name}")

            # Update the model in the registry
            self.model_registry.update_model(model_name, model)
            return True
        except Exception as e:
            self.logger.error(f"Error during training of model {model_name}: {str(e)}")
            return False

    def evaluate_model(self, model_name: str, test_data: Any):
        model = self.model_registry.get_model(model_name)
        if not model:
            self.logger.error(f"Model {model_name} not found in registry")
            return None

        self.logger.info(f"Evaluating model: {model_name}")
        # Here you would actually evaluate the model using the test data
        # For simulation, we're just returning a dummy accuracy score
        accuracy = 0.85
        self.logger.info(f"Evaluation completed for model {model_name}. Accuracy: {accuracy}")
        return accuracy