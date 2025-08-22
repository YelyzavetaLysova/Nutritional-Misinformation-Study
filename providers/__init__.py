from .base import RecipeProvider, PreprocessProvider, ScoreProvider
from .dummy_provider import DummyRecipeProvider
from .grok_provider import GrokRecipeProvider
from .gemini_provider import GeminiRecipeProvider
from .deepseek_provider import DeepSeekRecipeProvider
from .perplexity_provider import PerplexityRecipeProvider
from .gpt5_provider import GPT5RecipeProvider

# Existing preprocess / score imports if already present
try:
    from .preprocess_provider import DefaultPreprocessProvider
    from .score_provider import FsaWhoScoreProvider
except Exception:
    DefaultPreprocessProvider = None
    FsaWhoScoreProvider = None

def get_recipe_provider(name: str) -> RecipeProvider | None:
    mapping = {
        "dummy": DummyRecipeProvider(),
        "grok": GrokRecipeProvider(),
        "gemini": GeminiRecipeProvider(),
        "deepseek": DeepSeekRecipeProvider(),
        "perplexity": PerplexityRecipeProvider(),
        "gpt5": GPT5RecipeProvider(),
    }
    return mapping.get(name)

def get_preprocess_provider():
    return DefaultPreprocessProvider() if DefaultPreprocessProvider else None

def get_score_provider():
    return FsaWhoScoreProvider() if FsaWhoScoreProvider else None