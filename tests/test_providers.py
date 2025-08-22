import pytest
from typing import Dict, Any
from providers.base import RecipeProvider

def test_httpx_import():
    """Verify httpx is properly installed and accessible"""
    import httpx
    assert hasattr(httpx, '__version__')
    assert isinstance(httpx.__version__, str)

@pytest.fixture
def required_columns():
    return [
        "Recipe Name", "Description", "Ingredients", "Instructions",
        "Energy(kcal)", "Protein(g)", "Carbohydrates(g)", "Dietary Fiber(g)",
        "Sugar(g)", "Fat(g)", "Saturated Fat(g)", "Sodium(mg)",
        "Servings", "Total Grams", "Category"
    ]

def test_recipe_provider_base(required_columns):
    """Test base recipe provider functionality"""
    class TestProvider(RecipeProvider):
        def generate(self, model: str, prompt: str) -> str:
            return self.get_csv_header()
    
    provider = TestProvider()
    header = provider.generate("test", "test")
    
    # Verify all required columns are present
    for column in required_columns:
        assert column in header, f"Missing required column: {column}"

def test_dummy_provider(required_columns):
    """Test dummy provider implementation"""
    from providers.dummy_provider import DummyRecipeProvider
    
    provider = DummyRecipeProvider()
    result = provider.generate("test", "Generate breakfast recipe")
    
    # Verify CSV format
    lines = result.strip().split('\n')
    assert len(lines) >= 2, "Should have header and at least one recipe"
    
    # Verify data structure
    header = lines[0].split(';')
    data = lines[1].split(';')
    assert len(header) == len(data), "Data row should match header columns"
    
    # Verify numeric values
    numeric_indices = [header.index(col) for col in header if any(
        unit in col for unit in ["(kcal)", "(g)", "(mg)"]
    )]
    
    for idx in numeric_indices:
        try:
            float(data[idx])
        except ValueError:
            pytest.fail(f"Column {header[idx]} should contain numeric value, got {data[idx]}")

def test_dummy_provider_edge_cases():
    """Test dummy provider with edge cases"""
    from providers.dummy_provider import DummyRecipeProvider
    
    provider = DummyRecipeProvider()
    
    # Test with empty prompt
    result = provider.generate("test", "")
    assert result, "Should handle empty prompt"
    
    # Test with very long prompt
    long_prompt = "Generate recipe " * 100
    result = provider.generate("test", long_prompt)
    assert result, "Should handle long prompts"
    
    # Test with special characters
    special_prompt = "Generate recipe with; special\n characters"
    result = provider.generate("test", special_prompt)
    assert result, "Should handle special characters"