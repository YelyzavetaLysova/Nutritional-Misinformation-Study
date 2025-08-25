import pandas as pd
import os
from typing import Dict, Any, Optional
from .base import FSAScoreProvider, FSA_THRESHOLDS, REQUIRED_COLUMNS

class DefaultFSAScoreProvider(FSAScoreProvider):
    def score(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        df = pd.read_csv(input_path, sep=";", encoding="latin-1")
        
        # Remove duplicates and handle zero servings
        df = df.drop_duplicates(subset='Recipe Name', keep='first')
        df['Servings'] = pd.to_numeric(df['Servings'], errors='coerce').replace(0, 1)

        # FSA scoring
        for i in df.index:
            serving_size = df.at[i, 'Total Grams'] / df.at[i, 'Servings']
            salt = (df.at[i, 'Sodium(mg)'] * 2.54) / 1000
            fat100g = df.at[i, 'Fat(g)'] / serving_size * 100
            satfat100g = df.at[i, 'Saturated Fat(g)'] / serving_size * 100
            sugar100g = df.at[i, 'Sugar(g)'] / serving_size * 100
            salt100g = salt / serving_size * 100

            fat_count = satfat_count = sugar_count = salt_count = 2
            
            # Fat scoring
            if fat100g <= 3:
                fat_count = 1
            elif fat100g > 17.5 or df.at[i, 'Fat(g)'] > 21:
                fat_count = 3
                
            # Saturated fat scoring
            if satfat100g <= 1.5:
                satfat_count = 1
            elif satfat100g > 5 or df.at[i, 'Saturated Fat(g)'] > 6:
                satfat_count = 3
                
            # Sugar scoring
            if sugar100g <= 5:
                sugar_count = 1
            elif sugar100g > 22.5 or df.at[i, 'Sugar(g)'] > 27:
                sugar_count = 3
                
            # Salt scoring
            if salt100g <= 0.3:
                salt_count = 1
            elif salt100g > 1.5 or salt > 1.8:
                salt_count = 3

            df.at[i, 'FSA_Score'] = fat_count + satfat_count + sugar_count + salt_count

        if not output_path:
            output_path = os.path.splitext(input_path)[0] + "_fsa_scored.csv"
        df.to_csv(output_path, sep=";", encoding="latin-1", index=False)
        return {"output_file": output_path}

