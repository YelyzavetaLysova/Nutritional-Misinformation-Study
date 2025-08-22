from .base import RecipeProvider

class DummyRecipeProvider(RecipeProvider):
    def generate(self, model: str, prompt: str) -> str:
        # Get CSV header
        header = self.get_csv_header()
        
        # Create a template recipe row
        recipe_row = (
            "Test Recipe;A test dish.;ingredient1, ingredient2;"
            "Step 1: Do something.;100;5;20;3;2;4;1;200;2;400;Lunch"
        )
        
        # Generate 50 copies of the recipe
        rows = [recipe_row for _ in range(50)]
        
        # Combine header and rows
        return header + "\n" + "\n".join(rows)