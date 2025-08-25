import os
import httpx
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import RecipeProvider  # Changed to relative import
from prompts import SYSTEM_PROMPT, get_recipe_prompt

class GPT5RecipeProvider(RecipeProvider):
    """OpenAI GPT provider implementation"""
    
    API_URL = "https://api.openai.com/v1/chat/completions"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate(self, model: str, prompt: str) -> str:
        api_key = os.getenv("GPT5_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return self._dummy_csv(prompt, note="missing GPT5_API_KEY/OPENAI_API_KEY")

        try:
            with httpx.Client(timeout=self.timeout) as client:
                r = client.post(
                    self.API_URL,
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": get_recipe_prompt(prompt)}
                        ],
                        "temperature": 0.7
                    },
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                )
                r.raise_for_status()
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return self._dummy_csv(prompt, note=f"gpt5 error: {e}")

    def _parse_recipes(self, content: str) -> list[Dict[str, Any]]:
        # Add recipe parsing logic
        pass

    def _format_csv(self, recipes: list[Dict[str, Any]]) -> str:
        header = self.get_csv_header()
        rows = []
        for recipe in recipes:
            row = (
                f"{recipe['name']};{recipe['description']};"
                f"{','.join(recipe['ingredients'])};"
                f"{','.join(recipe['instructions'])};"
                f"{recipe['nutrition']['energy_kcal']};"
                f"{recipe['nutrition']['protein_g']};"
                f"{recipe['nutrition']['carbohydrates_g']};"
                f"{recipe['nutrition']['dietary_fiber_g']};"
                f"{recipe['nutrition']['sugar_g']};"
                f"{recipe['nutrition']['fat_g']};"
                f"{recipe['nutrition']['saturated_fat_g']};"
                f"{recipe['nutrition']['sodium_mg']};"
                f"{recipe['servings']};{recipe['total_grams']};"
                f"{recipe['category']}"
            )
            rows.append(row)
        return header + "\n" + "\n".join(rows)