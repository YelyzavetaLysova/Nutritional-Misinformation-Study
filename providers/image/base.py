from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ImageProvider(ABC):
    """Base class for recipe image generation"""
    
    @abstractmethod
    def generate_images(self, recipe_data: Dict[str, Any]) -> List[str]:
        """
        Generate images for recipes
        
        Args:
            recipe_data: Dictionary containing recipe information
            
        Returns:
            List of paths to generated images
        """
        pass