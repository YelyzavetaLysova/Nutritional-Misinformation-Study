from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class NutritionValues(BaseModel):
    """Just validate data format, not scores"""
    energy_kcal: float = Field(gt=0)
    protein_g: float = Field(ge=0)
    carbohydrates_g: float = Field(ge=0)
    dietary_fiber_g: float = Field(ge=0)
    sugar_g: float = Field(ge=0)
    fat_g: float = Field(ge=0)
    saturated_fat_g: float = Field(ge=0)
    sodium_mg: float = Field(ge=0)

class Recipe(BaseModel):
    name: str
    description: str
    ingredients: list[str]
    instructions: list[str]
    nutrition: NutritionValues
    category: str
    servings: int = Field(gt=0)
    total_grams: float = Field(gt=0)

class RecipeProvider(ABC):
    def __init__(self):
        self.retry_count = 3
        self.timeout = 60
    
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
    
    def validate_recipe(self, recipe_data: Dict[str, Any]) -> bool:
        try:
            Recipe(**recipe_data)
            return True
        except Exception as e:
            return False

class PreprocessProvider(ABC):
    @abstractmethod
    def preprocess(self, input_path: str, output_path: Optional[str] = None) -> str:
        pass

class ScoreProvider(ABC):
    @abstractmethod
    def score(self, input_path: str, output_path: Optional[str] = None) -> dict:
        pass