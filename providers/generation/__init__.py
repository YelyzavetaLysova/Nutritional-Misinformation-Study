from typing import Optional
from .base import RecipeProvider
from .gpt5_provider import GPT5RecipeProvider
from .grok_provider import GrokRecipeProvider
from .gemini_provider import GeminiRecipeProvider
from .deepseek_provider import DeepSeekRecipeProvider
from .perplexity_provider import PerplexityRecipeProvider
from .dummy_provider import DummyRecipeProvider

# Existing preprocess / score imports if already present
try:
    from ..preprocessing.preprocess_provider import DefaultPreprocessProvider
    from ..scoring import FsaWhoScoreProvider
except Exception:
    DefaultPreprocessProvider = None
    FsaWhoScoreProvider = None

def get_recipe_provider(provider_name: str) -> Optional[RecipeProvider]:
    """Get recipe provider by name"""
    providers = {
        'gpt5': GPT5RecipeProvider,
        'grok': GrokRecipeProvider,
        'gemini': GeminiRecipeProvider,
        'deepseek': DeepSeekRecipeProvider,
        'perplexity': PerplexityRecipeProvider,
        'dummy': DummyRecipeProvider
    }
    provider_class = providers.get(provider_name.lower())
    return provider_class() if provider_class else None

def get_preprocess_provider():
    return DefaultPreprocessProvider() if DefaultPreprocessProvider else None

def get_score_provider():
    return FsaWhoScoreProvider() if FsaWhoScoreProvider else None