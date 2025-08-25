import logging
import os
from datetime import datetime
from abc import ABC, abstractmethod
from .base import LoggingProvider

class LoggingProvider(ABC):
    @abstractmethod
    def log_generation(self, provider: str, status: str) -> None:
        pass

    @abstractmethod
    def log_validation(self, recipe_id: str, is_valid: bool) -> None:
        pass

class DefaultLoggingProvider(LoggingProvider):
    def __init__(self):
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.log_dir, 'api.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def log_request(self, path: str, method: str, status_code: int) -> None:
        self.logger.info(
            f"Request: {method} {path} - Status: {status_code}"
        )

    def log_error(self, error: str) -> None:
        self.logger.error(f"Error: {error}")