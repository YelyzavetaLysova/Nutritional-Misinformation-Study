from typing import Dict

# System prompt for recipe generation
SYSTEM_PROMPT = """You are a chef that will provide recipe recommendations. The recommendations should include Recipe name, a description of the dish, ingredients, detailed instructions on how to make the dish, Energy(kcal), Protein (g), Carbohydrates(g), Dietary Fiber (g), Sugar(g), Fat(g), Saturated Fat(g), Sodium(mg), Servings, Total Grams and food category, either Breakfast, Lunch, Dinner, Desserts, Snacks. The output should be in a CSV format, separated with ;."""

EXAMPLE_RECIPE = """Quinoa Salad with Chickpeas and Vegetables; A vibrant, nutrient-packed dish that's perfect for a light lunch or side.; 1 cup quinoa, uncooked. 1 ½ cups water. 1 cup canned chickpeas, rinsed and drained. 1 medium cucumber, diced. 1 medium red bell pepper, diced. 1 cup cherry tomatoes, halved. ¼ cup red onion, finely chopped. 2 tablespoons olive oil. 1 tablespoon lemon juice, 1 teaspoon cumin powder, Salt and pepper to taste, 2 tablespoons fresh parsley; 1. Rinse the quinoa under cold water in a fine mesh sieve. 2. In a medium pot, combine quinoa and water. Bring to a boil, reduce heat to low, cover, and simmer for 15 minutes or until the water is absorbed. Fluff with a fork and let it cool. 3. In a large mixing bowl, combine the cooked quinoa, chickpeas, cucumber, bell pepper, cherry tomatoes, and red onion. 4. In a small bowl, whisk together olive oil, lemon juice, cumin, salt, and pepper. Pour over the salad and toss to combine. 5. Sprinkle with parsley if desired, and serve chilled or at room temperature.;240;7.5;31;5;3;9.5;1.3;140;4;1340;Lunch"""

def get_recipe_prompt(meal: str) -> str:
    """
    Generate a prompt for recipe creation based on meal type.
    
    Args:
        meal (str): The type of meal to generate recipes for
        
    Returns:
        str: Formatted prompt with example recipe
    """
    return f"Create 5 recipes for {meal}. Follow this example: {EXAMPLE_RECIPE} Do not add anything else that is not stated. Never use ; other then separating the columns."

def get_csv_header() -> str:
    """
    Get the CSV header format for recipe data.
    
    Returns:
        str: CSV header string with column names
    """
    return (
        "Recipe Name;Description;Ingredients;Instructions;"
        "Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);"
        "Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);"
        "Servings;Total Grams;Category"
    )

# Recipe format validation constants
MIN_ENERGY_KCAL = 50
MAX_ENERGY_KCAL = 2000
MIN_SERVINGS = 1
MAX_SERVINGS = 12
MIN_TOTAL_GRAMS = 100
MAX_TOTAL_GRAMS = 5000