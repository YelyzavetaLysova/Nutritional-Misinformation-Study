from abc import ABC, abstractmethod
from typing import Optional

class RecipeProvider(ABC):
    @abstractmethod
    def generate(self, model: str, prompt: str) -> str:
        pass

    def get_csv_header(self) -> str:
        """Return standard CSV header for recipes"""
        return (
            "Recipe Name;Description;Ingredients;Instructions;Energy(kcal);"
            "Protein(g);Carbohydrates(g);Dietary Fiber(g);Sugar(g);Fat(g);"
            "Saturated Fat(g);Sodium(mg);Servings;Total Grams;Category"
        )

class PreprocessProvider(ABC):
    @abstractmethod
    def preprocess(self, input_path: str, output_path: Optional[str] = None) -> str:
        pass

class ScoreProvider(ABC):
    @abstractmethod
    def score(self, input_path: str, output_path: Optional[str] = None) -> dict:
        pass