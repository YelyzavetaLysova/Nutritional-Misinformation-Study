import os
import openai
from .base import RecipeProvider

class OpenAIRecipeProvider(RecipeProvider):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self.client = openai.OpenAI(api_key=api_key)

    def generate(self, model: str, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a chef that will provide recipe recommendations. The recommendations should include Recipe name, a description of the dish, ingredients, detailed instructions on how to make the dish, Energy(kcal), Protein (g), Carbohydrates(g), Dietary Fiber (g), Sugar(g), Fat(g), Saturated Fat(g), Sodium(mg), Servings, Total Grams and food category, either Breakfast, Lunch, Dinner, Desserts, Snacks. The output should be in a CSV format, separated with ;."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content