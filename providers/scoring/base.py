from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

# Required columns for scoring
REQUIRED_COLUMNS = {
    'Recipe Name', 'Total Grams', 'Servings',
    'Energy(kcal)', 'Protein(g)', 'Carbohydrates(g)',
    'Dietary Fiber(g)', 'Sugar(g)', 'Fat(g)',
    'Saturated Fat(g)', 'Sodium(mg)'
}

# FSA scoring thresholds
FSA_THRESHOLDS = {
    'fat_low': 3.0,
    'fat_high': 17.5,
    'satfat_low': 1.5,
    'satfat_high': 5.0,
    'sugar_low': 5.0,
    'sugar_high': 22.5,
    'salt_low': 0.3,
    'salt_high': 1.5
}

# WHO scoring thresholds
WHO_THRESHOLDS = {
    'protein_energy': 10.0,
    'fat_energy': 30.0,
    'fibre': 25.0,
    'satfat_energy': 10.0,
    'carbs_energy': 75.0,
    'sugar_energy': 10.0,
    'salt': 5.0
}

class FSAScoreProvider(ABC):
    """Base class for FSA scoring implementation"""
    
    @abstractmethod
    def score(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Calculate FSA scores for recipes"""
        pass

class WHOScoreProvider(ABC):
    """Base class for WHO scoring implementation"""
    
    @abstractmethod
    def score(self, input_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Calculate WHO scores for recipes"""
        pass
