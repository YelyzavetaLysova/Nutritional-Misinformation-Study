from .fsa_provider import DefaultFSAScoreProvider
from .who_provider import DefaultWHOScoreProvider

def get_score_provider(type: str = "fsa") -> "DefaultFSAScoreProvider | DefaultWHOScoreProvider":
    """Get scoring provider based on type"""
    if type.lower() == "who":
        return DefaultWHOScoreProvider()
    return DefaultFSAScoreProvider()