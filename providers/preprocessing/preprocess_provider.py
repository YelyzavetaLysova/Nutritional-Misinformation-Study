import pandas as pd
from typing import Optional
from .base import PreprocessProvider  # This will now correctly import from local base.py

class DefaultPreprocessProvider(PreprocessProvider):
    """Implements exact preprocessing logic from old program"""
    
    def preprocess(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Preprocess recipe data following old program logic exactly
        
        Args:
            input_path: Path to input CSV file
            output_path: Optional path for output file
            
        Returns:
            str: Path to processed file
        """
        # Read with latin-1 encoding as in old program
        df = pd.read_csv(input_path, sep=";", encoding="latin-1")
        
        # Remove duplicates in Recipe Name, keeping first occurrence
        df = df.drop_duplicates(subset='Recipe Name', keep='first')
        
        # Convert numeric columns exactly as in old program
        numeric_columns = [
            'Energy(kcal)', 'Protein(g)', 'Carbohydrates(g)', 
            'Dietary Fiber(g)', 'Sugar(g)', 'Fat(g)', 
            'Saturated Fat(g)', 'Sodium(mg)', 'Servings', 'Total Grams'
        ]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Category preprocessing
        df['Category'] = df['Category'].astype(str).str.strip()
        
        # Exact replacements from old program
        replacements = {
            'Dinne': 'Dinner',
            'Luns': 'Lunch',
            'Breakfas': 'Breakfast',
            'Dessert': 'Desserts',
            'Snack': 'Snacks',
            'dinner': 'Dinner',
            'lunch': 'Lunch',
            'breakfast': 'Breakfast',
            'desserts': 'Desserts',
            'snacks': 'Snacks'
        }
        df['Category'] = df['Category'].replace(replacements)
        
        # Validate categories
        allowed_categories = {'Dinner', 'Lunch', 'Breakfast', 'Desserts', 'Snacks'}
        invalid_categories = df[~df['Category'].isin(allowed_categories)]['Category'].unique()
        if len(invalid_categories) > 0:
            print(f"Warning: Found invalid categories: {invalid_categories}")
        
        # Handle output path
        if not output_path:
            output_path = input_path.replace('.csv', '_preprocessed.csv')
            
        # Save with same encoding and separator as old program
        df.to_csv(output_path, sep=";", encoding="latin-1", index=False)
        return output_path