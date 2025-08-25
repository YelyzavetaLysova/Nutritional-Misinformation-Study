import os
import httpx
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import RecipeProvider
from prompts import SYSTEM_PROMPT, get_recipe_prompt

class PerplexityRecipeProvider(RecipeProvider):
    """Perplexity AI provider implementation"""
    
    API_URL = "https://api.perplexity.ai/chat/completions"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate(self, model: str, prompt: str) -> str:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            return self._dummy_csv(prompt, note="missing PERPLEXITY_API_KEY")

        try:
            with httpx.Client(timeout=self.timeout) as client:
                r = client.post(
                    self.API_URL,
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": get_recipe_prompt(prompt)}
                        ]
                    },
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                )
                r.raise_for_status()
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return self._dummy_csv(prompt, note=f"perplexity error: {e}")

    def _dummy_csv(self, text: str, note: str="") -> str:
        return (
            "Recipe Name;Description;Ingredients;Instructions;Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);Servings;Total Grams;Category\n"
            f"Perplexity Recipe;{note or 'Generated with Perplexity'};ingredientX, ingredientY;{text[:120]};130;9;15;2;5;6;2;190;2;420;Lunch"
        )