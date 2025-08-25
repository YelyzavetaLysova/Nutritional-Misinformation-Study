from .base import RecipeProvider

class DummyRecipeProvider(RecipeProvider):
    """Dummy provider for testing"""
    
    def generate(self, model: str, prompt: str) -> str:
        return self._dummy_csv(
            prompt, 
            note="This is a dummy response for testing purposes"
        )