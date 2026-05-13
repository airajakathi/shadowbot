# shadowbot/inc/__init__.py
# Lazy loading - ShadowBotModel is only imported when accessed
# This avoids the ~3500ms langchain_openai import at CLI startup

def __getattr__(name):
    """Lazy load ShadowBotModel only when accessed."""
    if name == "ShadowBotModel":
        from .models import ShadowBotModel
        return ShadowBotModel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["ShadowBotModel"]