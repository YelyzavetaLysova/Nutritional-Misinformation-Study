import os
import pandas as pd
from .base import PreprocessProvider
from preprocess import preprocess_csv  # uses your existing function

class DefaultPreprocessProvider(PreprocessProvider):
    def preprocess(self, input_path: str, output_path: str | None = None) -> str:
        return preprocess_csv(input_path, output_path)