from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class RecipeProvider(ABC):
    """Base class for recipe generation providers"""
    
    def __init__(self):
        self.timeout = 60  # Default timeout in seconds
        
    @abstractmethod
    def generate(self, model: str, prompt: str) -> str:
        """
        Generate recipes using AI provider
        
        Args:
            model: Model identifier to use
            prompt: Recipe generation prompt
            
        Returns:
            str: Generated recipes in CSV format
        """
        pass
    
    def get_csv_header(self) -> str:
        """Return standard CSV header for recipes"""
        return (
            "Recipe Name;Description;Ingredients;Instructions;"
            "Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);"
            "Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);"
            "Servings;Total Grams;Category"
        )
    
    def _dummy_csv(self, text: str, note: str = "") -> str:
        """Generate dummy CSV response for error cases"""
        return (
            f"{self.get_csv_header()}\n"
            f"Dummy Recipe;{note or 'Fallback response'};ingredient1, ingredient2;"
            f"{text[:120]};100;5;20;3;2;4;1;200;2;400;Lunch"
        )