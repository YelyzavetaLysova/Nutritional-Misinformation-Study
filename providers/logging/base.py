from abc import ABC, abstractmethod
from typing import Optional

class LoggingProvider(ABC):
    """Base class for request and error logging"""
    
    @abstractmethod
    def log_request(self, path: str, method: str, status_code: int) -> None:
        """Log API request details"""
        pass
    
    @abstractmethod
    def log_error(self, error: str) -> None:
        """Log error details"""
        pass