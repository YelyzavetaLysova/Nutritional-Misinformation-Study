import pandas as pd


csv_file = r'C:\Users\47950\PycharmProjects\Master\cleaned_Vegan_data.csv'
df = pd.read_csv(csv_file, sep=";", encoding="latin-1")

# Remove duplicates in 'Recipe Name', keeping the first occurrence
df = df.drop_duplicates(subset='Recipe Name', keep='first')

# any occurrance of 0 in serving turns to 1. 
df['Servings'] = df['Servings'].replace(0, 1)
for i in df.index:
    serving_size = df.at[i,'Total Grams'] / df.at[i,'Servings']
    salt = (df.at[i, 'Sodium(mg)'] / 1000) * 2.54
    fat100g = df.at[i, 'Fat(g)'] / serving_size * 100
    satfat100g = df.at [i, 'Saturated Fat(g)'] /serving_size * 100
    sugar100g = df.at [i, 'Sugar(g)'] / serving_size * 100
    salt100g = salt / serving_size * 100
    fat_count = satfat_count = sugar_count = salt_count = 2
    if fat100g <= 3:
        fat_count = 1
    if fat100g > 17.5 or df.at[i,'Fat(g)'] > 21:
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
    df.at[i,'Fsa_new'] = fat_count + satfat_count + sugar_count + salt_count
    df.at[i, 'fat_count'] = fat_count
    df.at[i, 'satfat_count'] = satfat_count
    df.at[i, 'sugar_count'] = sugar_count
    df.at[i, 'salt_count'] = salt_count


for i in df.index:
    prot_count = fat2_count = fibre_count = satfat2_count = carb_count = sugar2_count = salt2_count = 0
    diatary_fibre = df.at[i, "Dietary Fiber(g)"] / df.at [i, "Servings"]
    energy = df.at[i, "Energy(kcal)"] / df.at[i, "Servings"]
    fat = df.at[i, "Fat(g)"] / df.at[i, "Servings"]
    satfat = df.at[i, "Saturated Fat(g)"] / df.at[i, "Servings"]
    sugar = df.at[i, "Sugar(g)"] / df.at[i, "Servings"]
    carb = df.at[i, "Carbohydrates(g)"] / df.at[i, "Servings"]
    protein = df.at[i, "Protein(g)"] / df.at[i, "Servings"]
    sodium = (df.at[i, "Sodium(mg)"] * 1000) / df.at[i, "Servings"]
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
    if sodium <= 2:
        salt2_count = 1
    if diatary_fibre > 20:
        fibre_count = 1
    df.at [i, "WHO Score"] = prot_count + fat2_count + fibre_count + satfat2_count + carb_count + sugar2_count + salt2_count
    df.at [i, "prot_count"] = prot_count
    df.at [i, "fat2_count"] = fat2_count
    df.at [i, "fibre_count"] = fibre_count
    df.at [i, "carb_count"] = carb_count
    df.at [i, "satfat2_count"] = satfat2_count
    df.at [i, "sugar2_count"] = sugar2_count
    df.at [i, "salt2_count"] = salt2_count








df.to_csv("cleaned_Vegan_data.csv", sep=";", encoding="latin-1", index=False)