import os
import httpx
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import RecipeProvider
from prompts import SYSTEM_PROMPT, get_recipe_prompt  # Changed from relative to absolute

class GeminiRecipeProvider(RecipeProvider):
    """
    Google Gemini provider.
    Set GEMINI_API_KEY env var.
    Uses generative language API (placeholder endpoint).
    """
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate(self, model: str, prompt: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return self._dummy_csv(prompt, note="missing GEMINI_API_KEY")

        try:
            with httpx.Client(timeout=self.timeout) as client:
                r = client.post(
                    f"{self.API_URL}?key={api_key}",
                    json={
                        "contents": [
                            {"role": "system", "parts": [{"text": SYSTEM_PROMPT}]},
                            {"role": "user", "parts": [{"text": get_recipe_prompt(prompt)}]}
                        ]
                    }
                )
                r.raise_for_status()
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return self._dummy_csv(prompt, note=f"gemini error: {e}")

    def _dummy_csv(self, text: str, note: str = "") -> str:
        return (
            "Recipe Name;Description;Ingredients;Instructions;Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);Servings;Total Grams;Category\n"
            f"Gemini Recipe;{note or 'Generated with Gemini'};ingredient1, ingredient2;{text[:120]};120;6;18;4;3;5;1;210;2;380;Dinner"
        )