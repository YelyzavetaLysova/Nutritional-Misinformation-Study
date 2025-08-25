import pandas as pd
from typing import Dict, Any, Set
from .base import ValidationProvider

class DefaultValidationProvider(ValidationProvider):
    def __init__(self):
        self.required_columns = {
            'Recipe Name', 'Description', 'Ingredients', 'Instructions',
            'Energy(kcal)', 'Protein(g)', 'Carbohydrates(g)', 'Dietary Fiber(g)',
            'Sugar(g)', 'Fat(g)', 'Saturated Fat(g)', 'Sodium(mg)',
            'Servings', 'Total Grams', 'Category'
        }
        self.allowed_categories = {'Breakfast', 'Lunch', 'Dinner', 'Desserts', 'Snacks'}

    def validate(self, input_path: str) -> Dict[str, Any]:
        df = pd.read_csv(input_path, sep=";", encoding="latin-1")
        
        results = {
            "missing_columns": self._check_columns(df.columns),
            "invalid_categories": self._check_categories(df['Category']),
            "null_values": self._check_nulls(df),
            "numeric_errors": self._check_numeric_values(df)
        }
        
        results["is_valid"] = all(not v for v in results.values())
        return results

    def _check_columns(self, columns: Set[str]) -> Set[str]:
        return self.required_columns - set(columns)

    def _check_categories(self, categories: pd.Series) -> Set[str]:
        return set(categories.unique()) - self.allowed_categories

    def _check_nulls(self, df: pd.DataFrame) -> Dict[str, int]:
        return {col: df[col].isnull().sum() for col in df.columns if df[col].isnull().any()}

    def _check_numeric_values(self, df: pd.DataFrame) -> Dict[str, int]:
        numeric_cols = [
            'Energy(kcal)', 'Protein(g)', 'Carbohydrates(g)', 'Dietary Fiber(g)',
            'Sugar(g)', 'Fat(g)', 'Saturated Fat(g)', 'Sodium(mg)',
            'Servings', 'Total Grams'
        ]
        errors = {}
        for col in numeric_cols:
            invalid = df[~df[col].apply(lambda x: isinstance(x, (int, float)))].shape[0]
            if invalid > 0:
                errors[col] = invalid
        return errors