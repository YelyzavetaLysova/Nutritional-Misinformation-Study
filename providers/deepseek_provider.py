import os
import httpx
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import RecipeProvider
# Change this line:
from prompts import SYSTEM_PROMPT, get_recipe_prompt  # Use absolute import

class DeepSeekRecipeProvider(RecipeProvider):
    """
    DeepSeek provider implementation.
    Requires DEEPSEEK_API_KEY environment variable.
    """
    API_URL = "https://api.deepseek.com/chat/completions"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate(self, model: str, prompt: str) -> str:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return self._dummy_csv(prompt, note="missing DEEPSEEK_API_KEY")

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
            return self._dummy_csv(prompt, note=f"deepseek error: {e}")

    def _format_content(self, content: str) -> str:
        """Format API response into CSV"""
        header = self.get_csv_header()
        # Basic content cleanup
        content = content.strip()
        if not content:
            return self._dummy_csv("empty response")
        return f"{header}\n{content}"