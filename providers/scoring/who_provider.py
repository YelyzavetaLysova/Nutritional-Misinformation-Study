import pandas as pd
import os
from typing import Dict, Any, Optional
from .base import WHOScoreProvider, WHO_THRESHOLDS, REQUIRED_COLUMNS

class DefaultWHOScoreProvider(WHOScoreProvider):
    def score(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        df = pd.read_csv(input_path, sep=";", encoding="latin-1")
        df = df.drop_duplicates(subset='Recipe Name', keep='first')

        # WHO scoring
        for i in df.index:
            energy = df.at[i, 'Energy(kcal)']
            protein = df.at[i, 'Protein(g)'] * 4
            fat = df.at[i, 'Fat(g)'] * 9
            satfat = df.at[i, 'Saturated Fat(g)'] * 9
            carbs = df.at[i, 'Carbohydrates(g)'] * 4
            sugar = df.at[i, 'Sugar(g)'] * 4
            fibre = df.at[i, 'Dietary Fiber(g)']
            salt = (df.at[i, 'Sodium(mg)'] * 2.54) / 1000

            prot_count = fat2_count = fibre_count = 0
            satfat2_count = carb_count = sugar2_count = salt2_count = 0
            
            # WHO thresholds
            if protein/energy*100 >= 10:
                prot_count = 1
            if fat/energy*100 <= 30:
                fat2_count = 1
            if fibre >= 25:
                fibre_count = 1
            if satfat/energy*100 <= 10:
                satfat2_count = 1
            if carbs/energy*100 <= 75:
                carb_count = 1
            if sugar/energy*100 <= 10:
                sugar2_count = 1
            if salt <= 5:
                salt2_count = 1

            df.at[i, 'WHO_Score'] = (
                prot_count + fat2_count + fibre_count + 
                satfat2_count + carb_count + sugar2_count + salt2_count
            )

        if not output_path:
            output_path = os.path.splitext(input_path)[0] + "_who_scored.csv"
        df.to_csv(output_path, sep=";", encoding="latin-1", index=False)
        return {"output_file": output_path}

