import os
import google.generativeai as genai
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import RecipeProvider
from prompts import SYSTEM_PROMPT, get_recipe_prompt

class GeminiRecipeProvider(RecipeProvider):
    """Google Gemini provider implementation"""
    
    def __init__(self):
        super().__init__()
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate(self, model: str, prompt: str) -> str:
        if not os.getenv("GEMINI_API_KEY"):
            return self._dummy_csv(prompt, note="missing GEMINI_API_KEY")

        try:
            model = genai.GenerativeModel(model)
            response = model.generate_content(
                [SYSTEM_PROMPT, get_recipe_prompt(prompt)]
            )
            return response.text
        except Exception as e:
            return self._dummy_csv(prompt, note=f"gemini error: {e}")

    def _dummy_csv(self, text: str, note: str = "") -> str:
        return (
            "Recipe Name;Description;Ingredients;Instructions;Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);Servings;Total Grams;Category\n"
            f"Gemini Recipe;{note or 'Generated with Gemini'};ingredient1, ingredient2;{text[:120]};120;6;18;4;3;5;1;210;2;380;Dinner"
        )