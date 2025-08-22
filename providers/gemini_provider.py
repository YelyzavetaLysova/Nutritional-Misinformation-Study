import os, httpx
from .base import RecipeProvider

class GeminiRecipeProvider(RecipeProvider):
    """
    Google Gemini provider.
    Set GEMINI_API_KEY env var.
    Uses generative language API (placeholder endpoint).
    """
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def generate(self, model: str, prompt: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return self._dummy_csv(prompt, note="missing GEMINI_API_KEY")
        try:
            url = self.API_URL.format(model=model)
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            with httpx.Client(timeout=60) as client:
                r = client.post(f"{url}?key={api_key}", json=payload)
            r.raise_for_status()
            data = r.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return self._dummy_csv(text)
        except Exception as e:
            return self._dummy_csv(prompt, note=f"gemini error: {e}")

    def _dummy_csv(self, text: str, note: str = "") -> str:
        return (
            "Recipe Name;Description;Ingredients;Instructions;Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);Servings;Total Grams;Category\n"
            f"Gemini Recipe;{note or 'Generated with Gemini'};ingredient1, ingredient2;{text[:120]};120;6;18;4;3;5;1;210;2;380;Dinner"
        )