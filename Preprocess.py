import pandas as pd

def preprocess_csv(input_path, output_path=None):
    df = pd.read_csv(input_path, sep=";", encoding="latin-1")
    df['Category'] = df['Category'].astype(str)
    print(df.columns)
    print(df.dtypes)

    df = df.drop_duplicates(subset='Recipe Name', keep='first')

    # Fixing any outlier that may occur
    replacements = {
        'Dinne': 'Dinner',
        'Luns': 'Lunch',
        'Breakfas': 'Breakfast',
        'Snack': 'Snacks',
        'Dessert': 'Desserts',
        'Side Dis': 'Snacks',
        'Side  ': 'Snacks',
        'Side Dish  ': 'Snacks',
        'Sides  ': 'Snacks',
        'Drinks  ': 'Snacks',
        'Lunsj': 'Lunch',
        'Lunsj  ': 'Lunch',
        'Luns': 'Lunch',
        'Lunc': 'Lunch',
        'Brunch  ': 'Lunch',
        'Brunch': 'Lunch',
        'Breakfast  ': 'Breakfast',
        'Dinner  ': 'Dinner',
        'Lunch  ': 'Lunch',
        'Snacks  ': 'Snacks',
        'Desserts  ': 'Desserts',
        ' Desserts  ': 'Desserts',
        ' Dessert': 'Desserts',
        'Lunch ': 'Lunch',
        'Snacks ': 'Snacks'
    }
    df['Category'] = df['Category'].replace(replacements)

    allowed = {'Dinner', 'Lunch', 'Breakfast', 'Desserts', 'Snacks'}
    for dish in df["Category"]:
        words = dish.split()
        for word in words:
            if word not in allowed:
                print(f"Word not in allowed list: {word}")

    duplicates = df[df['Recipe Name'].duplicated()]
    print("Duplicate Recipe Names:")
    print(duplicates)

    if not output_path:
        output_path = input_path.replace('.csv', '_cleaned.csv')
    df.to_csv(output_path, sep=";", encoding="latin-1", index=False)
    print(f"Changes have been saved to '{output_path}'.")

# Example usage:
# preprocess_csv("RenalDiet_data.csv")

