from abc import ABC, abstractmethod

class RecipeProvider(ABC):
    @abstractmethod
    def generate(self, model: str, prompt: str) -> str:
        pass

class PreprocessProvider(ABC):
    @abstractmethod
    def preprocess(self, input_path: str, output_path: str | None = None) -> str:
        pass

class ScoreProvider(ABC):
    @abstractmethod
    def score(self, input_path: str, output_path: str | None = None) -> dict:
        pass