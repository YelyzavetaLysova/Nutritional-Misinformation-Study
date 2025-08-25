from .preprocess_provider import DefaultPreprocessProvider

def get_preprocess_provider() -> DefaultPreprocessProvider:
    return DefaultPreprocessProvider()