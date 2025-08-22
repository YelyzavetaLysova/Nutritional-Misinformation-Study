import os, httpx
from .base import RecipeProvider

class DeepSeekRecipeProvider(RecipeProvider):
    """
    DeepSeek provider (placeholder).
    Set DEEPSEEK_API_KEY env var.
    """
    API_URL = "https://api.deepseek.com/chat/completions"

    def generate(self, model: str, prompt: str) -> str:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return self._dummy_csv(prompt, note="missing DEEPSEEK_API_KEY")
        try:
            payload = {
                "model": model,
                "messages":[{"role":"user","content":prompt}],
                "temperature":0.7
            }
            with httpx.Client(timeout=60) as client:
                r = client.post(
                    self.API_URL,
                    json=payload,
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type":"application/json"},
                )
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            return self._dummy_csv(content)
        except Exception as e:
            return self._dummy_csv(prompt, note=f"deepseek error: {e}")

    def _dummy_csv(self, text: str, note: str="") -> str:
        return (
            "Recipe Name;Description;Ingredients;Instructions;Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);Servings;Total Grams;Category\n"
            f"DeepSeek Recipe;{note or 'Generated with DeepSeek'};ingredientA, ingredientB;{text[:120]};95;7;25;5;4;3;1;180;2;350;Snack"
        )