from .logging_provider import DefaultLoggingProvider

def get_logging_provider() -> DefaultLoggingProvider:
    return DefaultLoggingProvider()