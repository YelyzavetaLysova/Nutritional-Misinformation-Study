import pandas as pd


csv_file =r'C:\Users\47950\PycharmProjects\Master\RenalDiet_data.csv'



df = pd.read_csv(csv_file, sep=";", encoding="latin-1")
df['Category'] = df['Category'].astype(str)
print(df.columns)
print(df.dtypes)


df = df.drop_duplicates(subset='Recipe Name', keep='first')


df['Category'] = df['Category'].replace('Dinne', 'Dinner')
df['Category'] = df['Category'].replace('Luns', 'Lunch')
df['Category'] = df['Category'].replace('Breakfas', 'Breakfast')
df['Category'] = df['Category'].replace('Snack', 'Snacks')
df['Category'] = df['Category'].replace('Dessert', 'Desserts')
df['Category'] = df['Category'].replace('Side Dis', 'Snacks')
df['Category'] = df['Category'].replace('Side  ', 'Snacks')
df['Category'] = df['Category'].replace('Side Dish  ', 'Snacks')
df['Category'] = df['Category'].replace('Sides  ', 'Snacks')
df['Category'] = df['Category'].replace('Drinks  ', 'Snacks')
df['Category'] = df['Category'].replace('Lunsj', 'Lunch')
df['Category'] = df['Category'].replace('Lunsj  ', 'Lunch')
df['Category'] = df['Category'].replace('Luns', 'Lunch')
df['Category'] = df['Category'].replace('Lunc', 'Lunch')
df['Category'] = df['Category'].replace('Brunch  ', 'Lunch')
df['Category'] = df['Category'].replace('Brunch', 'Lunch')
df['Category'] = df['Category'].replace('Breakfast  ', 'Breakfast')
df['Category'] = df['Category'].replace('Dinner  ', 'Dinner')
df['Category'] = df['Category'].replace('Lunch  ', 'Lunch')
df['Category'] = df['Category'].replace('Snacks  ', 'Snacks')
df['Category'] = df['Category'].replace('Desserts  ', 'Desserts')
df['Category'] = df['Category'].replace(' Desserts  ', 'Desserts')
df['Category'] = df['Category'].replace(' Dessert', 'Desserts')
df['Category'] = df['Category'].replace('Lunch ', 'Lunch')
df['Category'] = df['Category'].replace('Snacks ', 'Snacks')
allowed = {'Dinner', 'Lunch', 'Breakfast', 'Desserts', 'Lunch', "Snacks"}


for dish in df["Category"]:
    words = dish.split()
    for word in words:
        if word not in allowed:
            print(f"Word not in allowed list: {word}")


duplicates = df[df['Recipe Name'].duplicated()]
print("Duplicate Recipe Names:")
print(duplicates)


output_file = "cleaned_RenalDiet.csv"
df.to_csv(output_file, sep=";", encoding="latin-1", index=False)

print(f"Changes have been saved to '{output_file}'.")

