from dataclasses import dataclass
from typing import List, Dict

MEAL_CATEGORIES = {
    "Breakfast": [
        "Bagels", "Breakfast Burritos", "Breakfast Casseroles", 
        "Breakfast Potatoes", "French Toast", "Oatmeal", "Pancakes", 
        "Waffles", "Breakfast Sandwiches", "Eggs Benedict", "Granola",  
        "Breakfast Muffins", "Yogurt Parfaits"  
    ],
    "Lunch": [
        "Antipasti", "Appetizers and Snacks", "Burgers", "Burritos",
        "Chicken Salads", "Sandwiches", "Soups", "Salads", "Wraps",  
        "Quinoa Bowls", "Grain Bowls", "Poke Bowls"  
    ],
    "Dinner": [
        "Beef Recipes", "Chicken Parmesan", "Lasagna", "Pasta Carbonara",
        "Pizza", "Stir-Fries", "Sushi", "Tacos", "Salmon", "Risotto",  
        "Curry", "Roasted Vegetables", "Grilled Meats"  
    ],
    "Desserts": [
        "Angel Food Cakes", "Apple Pie", "Brownies", "Cheesecakes",
        "Chocolate Cakes", "Cookies", "Ice Cream", "Tiramisu", "Cupcakes",  
        "Fruit Tarts", "Puddings", "Mousses"  
    ],
    "Snacks": [
        "Energy Balls", "Hummus", "Nachos", "Popcorn", "Pretzels",
        "Smoothies", "Trail Mix", "Vegetable Dips", "Granola Bars",  
        "Roasted Nuts", "Fruit Leather", "Kale Chips"  
    ]
}

DIETARY_RESTRICTIONS = {
    "Vegetarian": True,
    "Vegan": True,
    "Gluten-Free": True,
    "Dairy-Free": True,
    "Low-Carb": True,
    "Heart-Healthy": True,
    "Diabetic-Friendly": True
}

EXAMPLE_RECIPE = """Quinoa Salad with Chickpeas and Vegetables; A vibrant, nutrient-packed dish that's perfect for a light lunch or side.; 1 cup quinoa, uncooked. 1 ½ cups water. 1 cup canned chickpeas, rinsed and drained. 1 medium cucumber, diced. 1 medium red bell pepper, diced. 1 cup cherry tomatoes, halved. ¼ cup red onion, finely chopped. 2 tablespoons olive oil. 1 tablespoon lemon juice, 1 teaspoon cumin powder, Salt and pepper to taste, 2 tablespoons fresh parsley; 1. Rinse the quinoa under cold water in a fine mesh sieve. 2. In a medium pot, combine quinoa and water. Bring to a boil, reduce heat to low, cover, and simmer for 15 minutes or until the water is absorbed. Fluff with a fork and let it cool. 3. In a large mixing bowl, combine the cooked quinoa, chickpeas, cucumber, bell pepper, cherry tomatoes, and red onion. 4. In a small bowl, whisk together olive oil, lemon juice, cumin, salt, and pepper. Pour over the salad and toss to combine. 5. Sprinkle with parsley if desired, and serve chilled or at room temperature.;240;7.5;31;5;3;9.5;1.3;140;4;1340;Lunch"""

@dataclass
class Recipe:
    """Recipe data model"""
    name: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    nutrition: Dict[str, float]
    category: str
    servings: int
    total_grams: float

def get_recipe_prompt(meal: str) -> str:
    """Generate prompt for recipe creation"""
    return f"Create 5 recipes for {meal}. Follow this example: {EXAMPLE_RECIPE} Do not add anything else that is not stated. Never use ; other then separating the columns."

meals_list = [
    meal for category in MEAL_CATEGORIES.values() 
    for meal in category
]