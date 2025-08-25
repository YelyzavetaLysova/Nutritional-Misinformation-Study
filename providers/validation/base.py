from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ValidationProvider(ABC):
    """Base class for data validation"""
    
    @abstractmethod
    def validate(self, input_path: str) -> Dict[str, Any]:
        """
        Validate recipe data format and content
        
        Args:
            input_path: Path to input CSV file
            
        Returns:
            Dict containing validation results
        """
        pass