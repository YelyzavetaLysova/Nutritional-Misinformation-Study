from abc import ABC, abstractmethod
from typing import Optional

class PreprocessProvider(ABC):
    """Base class for preprocessing providers"""
    
    @abstractmethod
    def preprocess(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Preprocess recipe data
        
        Args:
            input_path: Path to input CSV file
            output_path: Optional path for output file
            
        Returns:
            str: Path to processed file
        """
        pass