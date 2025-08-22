import os, httpx
from .base import RecipeProvider

class PerplexityRecipeProvider(RecipeProvider):
    """
    Perplexity AI provider (placeholder).
    Set PERPLEXITY_API_KEY env var.
    """
    API_URL = "https://api.perplexity.ai/chat/completions"

    def generate(self, model: str, prompt: str) -> str:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            return self._dummy_csv(prompt, note="missing PERPLEXITY_API_KEY")
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
            return self._dummy_csv(prompt, note=f"perplexity error: {e}")

    def _dummy_csv(self, text: str, note: str="") -> str:
        return (
            "Recipe Name;Description;Ingredients;Instructions;Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);Servings;Total Grams;Category\n"
            f"Perplexity Recipe;{note or 'Generated with Perplexity'};ingredientX, ingredientY;{text[:120]};130;9;15;2;5;6;2;190;2;420;Lunch"
        )