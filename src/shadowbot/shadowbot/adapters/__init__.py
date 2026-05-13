"""
ShadowBot Adapters - Implementations for core protocols.

This module provides concrete implementations of:
- Reader adapters (AutoReader, LlamaIndexReaderAdapter, MarkItDownReaderAdapter)
- Vector store adapters (ChromaAdapter, PineconeAdapter, etc.)
- Retriever implementations
- Reranker implementations
"""

# Lazy loading to avoid heavy imports at package load time
_LAZY_IMPORTS = {
    # Readers
    "AutoReader": ("shadowbot.adapters.readers", "AutoReader"),
    "MarkItDownReader": ("shadowbot.adapters.readers", "MarkItDownReader"),
    "TextReader": ("shadowbot.adapters.readers", "TextReader"),
    "DirectoryReader": ("shadowbot.adapters.readers", "DirectoryReader"),
    "register_default_readers": ("shadowbot.adapters.readers", "register_default_readers"),
    
    # Vector stores
    "ChromaVectorStore": ("shadowbot.adapters.vector_stores", "ChromaVectorStore"),
    "register_default_vector_stores": ("shadowbot.adapters.vector_stores", "register_default_vector_stores"),
    
    # Retrievers
    "BasicRetriever": ("shadowbot.adapters.retrievers", "BasicRetriever"),
    "FusionRetriever": ("shadowbot.adapters.retrievers", "FusionRetriever"),
    "register_default_retrievers": ("shadowbot.adapters.retrievers", "register_default_retrievers"),
    
    # Rerankers
    "LLMReranker": ("shadowbot.adapters.rerankers", "LLMReranker"),
    "register_default_rerankers": ("shadowbot.adapters.rerankers", "register_default_rerankers"),
}


def __getattr__(name: str):
    """Lazy load adapters."""
    if name in _LAZY_IMPORTS:
        module_path, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """List available attributes."""
    return list(_LAZY_IMPORTS.keys())


__all__ = list(_LAZY_IMPORTS.keys())
