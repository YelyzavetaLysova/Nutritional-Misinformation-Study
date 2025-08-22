import pandas as pd
import os

def score_recipes(input_path, output_path=None):
    df = pd.read_csv(input_path, sep=";", encoding="latin-1")

    # Remove duplicates in 'Recipe Name', keeping the first occurrence
    df = df.drop_duplicates(subset='Recipe Name', keep='first')

    # Convert columns to numeric
    df['Total Grams'] = pd.to_numeric(df['Total Grams'], errors='coerce')
    df['Servings'] = pd.to_numeric(df['Servings'], errors='coerce')
    df['Saturated Fat(g)'] = pd.to_numeric(df['Saturated Fat(g)'], errors='coerce')

    # Replace any occurrence of 0 in servings with 1
    df['Servings'] = df['Servings'].replace(0, 1)

    # FSA scoring
    for i in df.index:
        serving_size = df.at[i, 'Total Grams'] / df.at[i, 'Servings']
        salt = (df.at[i, 'Sodium(mg)'] * 2.54) / 1000
        fat100g = df.at[i, 'Fat(g)'] / serving_size * 100
        satfat100g = df.at[i, 'Saturated Fat(g)'] / serving_size * 100
        sugar100g = df.at[i, 'Sugar(g)'] / serving_size * 100
        salt100g = salt / serving_size * 100

        fat_count = satfat_count = sugar_count = salt_count = 2
        if fat100g <= 3:
            fat_count = 1
        if fat100g > 17.5 or df.at[i, 'Fat(g)'] > 21:
            fat_count = 3
        if satfat100g <= 1.5:
            satfat_count = 1
        if satfat100g > 5 or df.at[i, 'Saturated Fat(g)'] > 6:
            satfat_count = 3
        if sugar100g <= 3:
            sugar_count = 1
        if sugar100g > 22.5 or df.at[i, 'Sugar(g)'] > 27:
            sugar_count = 3
        if salt100g < 0.3:
            salt_count = 1
        if salt100g > 1.5 or salt > 1.8:
            salt_count = 3

        df.at[i, 'Fsa_new'] = fat_count + satfat_count + sugar_count + salt_count
        df.at[i, 'fat_count'] = fat_count
        df.at[i, 'satfat_count'] = satfat_count
        df.at[i, 'sugar_count'] = sugar_count
        df.at[i, 'salt_count'] = salt_count

    # WHO scoring
    for i in df.index:
        prot_count = fat2_count = fibre_count = satfat2_count = carb_count = sugar2_count = salt2_count = 0
        diatary_fibre = df.at[i, "Dietary Fiber(g)"] / df.at[i, "Servings"]
        energy = df.at[i, "Energy(kcal)"] / df.at[i, "Servings"]
        fat = df.at[i, "Fat(g)"] / df.at[i, "Servings"]
        satfat = df.at[i, "Saturated Fat(g)"] / df.at[i, "Servings"]
        sugar = df.at[i, "Sugar(g)"] / df.at[i, "Servings"]
        carb = df.at[i, "Carbohydrates(g)"] / df.at[i, "Servings"]
        protein = df.at[i, "Protein(g)"] / df.at[i, "Servings"]
        salt = (df.at[i, "Sodium(mg)"] * 2.5) / 1000
        salt_per_serving = salt / df.at[i, "Servings"]

        if 0.1 * energy <= protein * 4 <= 0.15 * energy:
            prot_count = 1
        if 0.15 * energy <= fat * 9 <= 0.3 * energy:
            fat2_count = 1
        if 0.1 * energy >= satfat * 9:
            satfat2_count = 1
        if 0.55 * energy <= carb * 4 <= 0.75 * energy:
            carb_count = 1
        if 0.1 * energy >= sugar * 4:
            sugar2_count = 1
        if salt_per_serving <= 0.2:
            salt2_count = 1
        if (energy * diatary_fibre) / 100 >= 3:
            fibre_count = 1

        df.at[i, "WHO Score"] = prot_count + fat2_count + fibre_count + satfat2_count + carb_count + sugar2_count + salt2_count
        df.at[i, "prot_count"] = prot_count
        df.at[i, "fat2_count"] = fat2_count
        df.at[i, "fibre_count"] = fibre_count
        df.at[i, "carb_count"] = carb_count
        df.at[i, "satfat2_count"] = satfat2_count
        df.at[i, "sugar2_count"] = sugar2_count
        df.at[i, "salt2_count"] = salt2_count

    # Save to output
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + "_scored.csv"
    df.to_csv(output_path, sep=";", encoding="latin-1", index=False)
    print(f"Scores saved to '{output_path}'.")

# Example usage:
# score_recipes("your_file.csv")