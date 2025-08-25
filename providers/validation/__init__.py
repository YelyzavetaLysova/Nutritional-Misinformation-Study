from .validation_provider import DefaultValidationProvider

def get_validation_provider() -> DefaultValidationProvider:
    return DefaultValidationProvider()