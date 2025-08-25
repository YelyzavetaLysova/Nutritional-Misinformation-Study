from .image_provider import DefaultImageProvider

def get_image_provider() -> DefaultImageProvider:
    return DefaultImageProvider()