import os, httpx
from .base import RecipeProvider

class GPT5RecipeProvider(RecipeProvider):
    """
    GPT-5 (OpenAI style) provider.
    Set OPENAI_API_KEY or GPT5_API_KEY.
    """
    API_URL = "https://api.openai.com/v1/chat/completions"

    def generate(self, model: str, prompt: str) -> str:
        api_key = os.getenv("GPT5_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return self._dummy_csv(prompt, note="missing GPT5_API_KEY/OPENAI_API_KEY")
        try:
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
            with httpx.Client(timeout=60) as client:
                r = client.post(
                    self.API_URL,
                    json=payload,
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                )
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            return self._dummy_csv(content)
        except Exception as e:
            return self._dummy_csv(prompt, note=f"gpt5 error: {e}")

    def _dummy_csv(self, text: str, note: str = "") -> str:
        return (
            "Recipe Name;Description;Ingredients;Instructions;Energy(kcal);Protein(g);Carbohydrates(g);Dietary Fiber(g);Sugar(g);Fat(g);Saturated Fat(g);Sodium(mg);Servings;Total Grams;Category\n"
            f"GPT5 Recipe;{note or 'Generated with GPT-5'};ingredient1, ingredient2;{text[:120]};110;8;22;4;5;4;1;205;2;390;Dinner"
        )