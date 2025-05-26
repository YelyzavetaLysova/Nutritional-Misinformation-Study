
# 📊 Recipe generator and evaluator

This project consists of three Python scripts designed to:
1. Automatically generate recipe data using OpenAI's GPT API.
2. Preprocess and clean recipe datasets.
3. Evaluate the healthiness of recipes based on FSA and WHO nutritional scoring systems.

---

## 🗂 Project Structure

```bash
.
├── gpt_API.py           # Recipe generator using GPT-4o-mini
├── FsaScore2.py         # Nutritional scoring using FSA & WHO guidelines
├── Preprocess.py        # Data cleaning and normalization
├── cleaned_Dairyfree.csv
├── cleaned_GlutenFree.csv
├── cleaned_Heart-Healthy.csv
├── cleaned_MainFile.csv
├── cleaned_RenalDiet.csv
├── cleaned_Vegan_data.csv
└── README.md
```

---

## 🧠 Script Descriptions

### `gpt_API.py`
Uses OpenAI's GPT API to generate 5 detailed recipes for each meal type from a predefined list. The script:
- Sends a prompt to the GPT-4o-mini model.
- Receives recipes in CSV format with nutritional information.
- Saves the output to `output.csv`.

> **Dependencies**: `openai`, `csv`, `pandas`

> ⚠️ **Note**: Make sure your `OPENAI_API_KEY` is securely stored (e.g., in environment variables or a `.env` file) instead of hardcoding it.

---

### `FsaScore2.py`
Processes a CSV file (`cleaned_Vegan_data.csv`) and scores each recipe using:
- **FSA (Food Standards Agency)** traffic light system.
- **WHO (World Health Organization)** dietary guidelines.

Adds multiple scoring columns (`Fsa_new`, `WHO Score`, etc.) to reflect the nutritional quality per 100g and per serving.

> **Dependencies**: `pandas`

---

### `preprocess.py`
Cleans and standardizes the `RenalDiet_data.csv` file by:
- Removing duplicate recipes.
- Normalizing inconsistent category names (e.g., "Luns" → "Lunch").
- Ensuring all categories fall within a valid set: `Breakfast`, `Lunch`, `Dinner`, `Snacks`, `Desserts`.

Saves the cleaned output to `cleaned_dataset.csv`.

> **Dependencies**: `pandas`

---

## 🚀 How to Run

1. **Set up environment**
    ```bash
    pip install openai, pandas
    ```

2. **Run GPT-based recipe generation**
    ```bash
    python gpt_API.py
    ```

3. **Score Vegan recipes**
    Ensure `cleaned_Vegan_data.csv` exists, then:
    ```bash
    python FsaScore2.py
    ```

4. **Preprocess Renal Diet data**
    Ensure `RenalDiet_data.csv` is available, then:
    ```bash
    python preprocess.py
    ```

---

## 📌 Notes

- Recipes are stored in CSV format using `;` as the delimiter.
- Nutrition values per 100g are used to calculate health scores.
- Ensure your data files are encoded in `latin-1`.

---

## 📁 Outputs

- `output5.csv` — Raw GPT-generated recipes.
- `cleaned_Vegan_data.csv` — Scored vegan recipes.
- `cleaned_RenalDiet.csv` — Cleaned and normalized renal diet data.

---
```python
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```
