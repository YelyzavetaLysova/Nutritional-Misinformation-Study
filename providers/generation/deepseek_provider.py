import os
import httpx
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import RecipeProvider  # Changed to relative import
from prompts import SYSTEM_PROMPT, get_recipe_prompt

class DeepSeekRecipeProvider(RecipeProvider):
    """DeepSeek AI provider implementation"""
    
    API_URL = "https://api.deepseek.com/v1/chat/completions"
    
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
                        "temperature": 0.7,
                        "max_tokens": 2000
                    },
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                )
                r.raise_for_status()
                
                # Extract and format response
                content = r.json()["choices"][0]["message"]["content"]
                return self._format_response(content)
                
        except Exception as e:
            return self._dummy_csv(prompt, note=f"deepseek error: {e}")
    
    def _format_response(self, content: str) -> str:
        """Format the API response into proper CSV format"""
        if not content.strip():
            return self._dummy_csv("empty response")
            
        # Add header if not present
        if not content.startswith("Recipe Name;"):
            content = f"{self.get_csv_header()}\n{content}"
            
        return content