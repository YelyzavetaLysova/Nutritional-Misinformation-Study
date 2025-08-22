import os
import pandas as pd
from .base import ScoreProvider

class FsaWhoScoreProvider(ScoreProvider):
    def score(self, input_path: str, output_path: str | None = None) -> dict:
        try:
            df = pd.read_csv(input_path, sep=";", encoding="latin-1")
            df = df.drop_duplicates(subset='Recipe Name', keep='first')

            numeric_cols = [
                "Total Grams","Servings","Saturated Fat(g)","Energy(kcal)","Protein(g)",
                "Carbohydrates(g)","Dietary Fiber(g)","Sugar(g)","Fat(g)","Sodium(mg)"
            ]
            for c in numeric_cols:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors='coerce')

            df['Servings'] = df['Servings'].replace(0, 1)

            # FSA scoring
            for i in df.index:
                servings = df.at[i, 'Servings'] or 1
                total_grams = df.at[i, 'Total Grams'] or 0
                if total_grams == 0:
                    continue
                serving_size = total_grams / servings
                salt_g = (df.at[i, 'Sodium(mg)'] * 2.54) / 1000
                fat100g = (df.at[i, 'Fat(g)'] / serving_size) * 100
                satfat100g = (df.at[i, 'Saturated Fat(g)'] / serving_size) * 100
                sugar100g = (df.at[i, 'Sugar(g)'] / serving_size) * 100
                salt100g = (salt_g / serving_size) * 100

                fat_count = satfat_count = sugar_count = salt_count = 2
                if fat100g <= 3: fat_count = 1
                if fat100g > 17.5 or df.at[i, 'Fat(g)'] > 21: fat_count = 3
                if satfat100g <= 1.5: satfat_count = 1
                if satfat100g > 5 or df.at[i, 'Saturated Fat(g)'] > 6: satfat_count = 3
                if sugar100g <= 3: sugar_count = 1
                if sugar100g > 22.5 or df.at[i, 'Sugar(g)'] > 27: sugar_count = 3
                if salt100g < 0.3: salt_count = 1
                if salt100g > 1.5 or salt_g > 1.8: salt_count = 3

                df.at[i, 'Fsa_new'] = fat_count + satfat_count + sugar_count + salt_count
                df.at[i, 'fat_count'] = fat_count
                df.at[i, 'satfat_count'] = satfat_count
                df.at[i, 'sugar_count'] = sugar_count
                df.at[i, 'salt_count'] = salt_count

            # WHO scoring
            for i in df.index:
                servings = df.at[i, 'Servings'] or 1
                energy = (df.at[i, 'Energy(kcal)'] or 0) / servings
                fat = (df.at[i, 'Fat(g)'] or 0) / servings
                satfat = (df.at[i, 'Saturated Fat(g)'] or 0) / servings
                sugar = (df.at[i, 'Sugar(g)'] or 0) / servings
                carb = (df.at[i, 'Carbohydrates(g)'] or 0) / servings
                protein = (df.at[i, 'Protein(g)'] or 0) / servings
                fibre = (df.at[i, 'Dietary Fiber(g)'] or 0) / servings
                salt_total = (df.at[i, 'Sodium(mg)'] * 2.5) / 1000
                salt_per_serving = salt_total / servings

                prot_count = 1 if 0.1 * energy <= protein * 4 <= 0.15 * energy else 0
                fat2_count = 1 if 0.15 * energy <= fat * 9 <= 0.3 * energy else 0
                satfat2_count = 1 if 0.1 * energy >= satfat * 9 else 0
                carb_count = 1 if 0.55 * energy <= carb * 4 <= 0.75 * energy else 0
                sugar2_count = 1 if 0.1 * energy >= sugar * 4 else 0
                salt2_count = 1 if salt_per_serving <= 0.2 else 0
                fibre_count = 1 if (energy * fibre) / 100 >= 3 else 0

                df.at[i, 'WHO Score'] = prot_count + fat2_count + fibre_count + satfat2_count + carb_count + sugar2_count + salt2_count
                df.at[i, 'prot_count'] = prot_count
                df.at[i, 'fat2_count'] = fat2_count
                df.at[i, 'fibre_count'] = fibre_count
                df.at[i, 'carb_count'] = carb_count
                df.at[i, 'satfat2_count'] = satfat2_count
                df.at[i, 'sugar2_count'] = sugar2_count
                df.at[i, 'salt2_count'] = salt2_count

            if not output_path:
                base, _ = os.path.splitext(input_path)
                if base.endswith("_preprocessed"):
                    base = base[:-13]
                output_path = base.replace("_raw", "") + "_scored.csv"

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, sep=";", encoding="latin-1", index=False)

            return {
                "status": "success",
                "output_path": output_path,
                "recipes_scored": len(df)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}