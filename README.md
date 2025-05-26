
# 🥗 Vegan Recipe Nutrition Scoring

This repository contains a Python script that processes a dataset of vegan recipes and computes two health scores—**FSA** and **WHO**—based on nutritional guidelines. The output is a cleaned and enriched CSV file, ready for further analysis or reporting.

---

## 📂 Features

✅ Removes duplicate recipes based on name  
✅ Fixes recipes with zero servings  
✅ Calculates nutrient values per 100g  
✅ Computes:
- 🔴 **FSA score** (fat, saturated fat, sugar, salt)
- 🌍 **WHO score** (protein, fat, fiber, carbs, sugar, sodium, sat. fat)

✅ Appends new scores and diagnostic columns to the CSV  
✅ Saves the processed file as `cleaned_Vegan_data.csv`

---

## 📊 Input Data Requirements

The input CSV must contain the following columns (semicolon `;` delimited, `latin-1` encoding):

| Column Name           | Description                        |
|-----------------------|------------------------------------|
| `Recipe Name`         | Name of the recipe                 |
| `Servings`            | Number of servings                 |
| `Total Grams`         | Total mass of the recipe (grams)   |
| `Sodium(mg)`          | Sodium content in milligrams       |
| `Fat(g)`              | Total fat in grams                 |
| `Saturated Fat(g)`    | Saturated fat in grams             |
| `Sugar(g)`            | Sugar content in grams             |
| `Energy(kcal)`        | Energy content in kcal             |
| `Carbohydrates(g)`    | Carbohydrates in grams             |
| `Protein(g)`          | Protein content in grams           |
| `Dietary Fiber(g)`    | Fiber content in grams             |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/vegan-nutrition-scoring.git
cd vegan-nutrition-scoring
```

### 2. Install dependencies
```bash
pip install pandas
```

### 3. Adjust the file path
Edit the `csv_file` variable in the script:
```python
csv_file = r'C:\path\to\cleaned_Vegan_data.csv'
```

### 4. Run the script
```bash
python nutrition_score.py
```

---

## 🧮 Scoring Logic

### 🔴 FSA Score
Based on UK Food Standards Agency (FSA) traffic light labeling:
- **Fat, Saturated Fat, Sugar, Salt**
- Each gets a score from 1 (low) to 3 (high)
- Total score = sum of all (range: 4–12)

### 🌍 WHO Score
Based on WHO dietary recommendations:
- Evaluates macronutrient-to-energy ratios
- Includes **fiber** and **sodium**
- Score from 0 to 7 (1 point per healthy criterion met)

---

## 📁 Output

The final CSV includes new columns:
- `Fsa_new`, `fat_count`, `satfat_count`, `sugar_count`, `salt_count`
- `WHO Score`, `prot_count`, `fat2_count`, `fibre_count`, `carb_count`, `satfat2_count`, `sugar2_count`, `salt2_count`

Saved as:  
```bash
cleaned_Vegan_data.csv
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙋‍♂️ Author

**[Your Name]**  
📧 your.email@example.com  
💼 [LinkedIn or Portfolio Link]
