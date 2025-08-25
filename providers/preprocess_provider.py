import os
import pandas as pd
from typing import Optional
from .base import PreprocessProvider

class DefaultPreprocessProvider(PreprocessProvider):
    """
    Default implementation of preprocessing provider.
    Handles data cleaning and standardization.
    """
    
    def preprocess(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Preprocess recipe data from CSV file.
        
        Args:
            input_path: Path to input CSV file
            output_path: Optional path for output file. If None, modifies input file
            
        Returns:
            str: Path to processed file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If CSV format is invalid
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        try:
            # Read CSV with proper encoding
            df = pd.read_csv(input_path, sep=";", encoding="utf-8")
            
            # Remove duplicates
            df = df.drop_duplicates(subset='Recipe Name', keep='first')
            
            # Convert numeric columns
            numeric_cols = [
                'Energy(kcal)', 'Protein(g)', 'Carbohydrates(g)', 
                'Dietary Fiber(g)', 'Sugar(g)', 'Fat(g)', 'Saturated Fat(g)',
                'Sodium(mg)', 'Servings', 'Total Grams'
            ]
            
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Handle missing values
            df = df.dropna(subset=['Recipe Name', 'Category'])
            
            # Save processed data
            output_file = output_path or input_path
            df.to_csv(output_file, sep=";", index=False)
            
            return output_file

        except Exception as e:
            raise ValueError(f"Failed to process file: {str(e)}")