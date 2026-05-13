"""
ShadowBot Knowledge - Advanced knowledge management system with configurable features.

This module provides:
- Document readers (ReaderProtocol, ReaderRegistry)
- Vector stores (VectorStoreProtocol, VectorStoreRegistry)
- Retrieval strategies (RetrieverProtocol, RetrievalStrategy)
- Rerankers (RerankerProtocol, RerankerRegistry)
- Index types (IndexProtocol, IndexType)
- Query engines (QueryEngineProtocol, QueryMode)
"""

# Core Knowledge class (always available)
from shadowbotagents.knowledge.knowledge import Knowledge
from shadowbotagents.knowledge.chunking import Chunking

# Lazy loading for protocols and registries to avoid import overhead
_LAZY_IMPORTS = {
    # Models and Protocols (new)
    "SearchResultItem": ("shadowbotagents.knowledge.models", "SearchResultItem"),
    "SearchResult": ("shadowbotagents.knowledge.models", "SearchResult"),
    "AddResult": ("shadowbotagents.knowledge.models", "AddResult"),
    "normalize_search_item": ("shadowbotagents.knowledge.models", "normalize_search_item"),
    "normalize_search_result": ("shadowbotagents.knowledge.models", "normalize_search_result"),
    "normalize_to_dict": ("shadowbotagents.knowledge.models", "normalize_to_dict"),
    "KnowledgeStoreProtocol": ("shadowbotagents.knowledge.protocols", "KnowledgeStoreProtocol"),
    "KnowledgeBackendError": ("shadowbotagents.knowledge.protocols", "KnowledgeBackendError"),
    "ScopeRequiredError": ("shadowbotagents.knowledge.protocols", "ScopeRequiredError"),
    "BackendNotAvailableError": ("shadowbotagents.knowledge.protocols", "BackendNotAvailableError"),
    
    # Readers
    "Document": ("shadowbotagents.knowledge.readers", "Document"),
    "ReaderProtocol": ("shadowbotagents.knowledge.readers", "ReaderProtocol"),
    "ReaderRegistry": ("shadowbotagents.knowledge.readers", "ReaderRegistry"),
    "get_reader_registry": ("shadowbotagents.knowledge.readers", "get_reader_registry"),
    "detect_source_kind": ("shadowbotagents.knowledge.readers", "detect_source_kind"),
    
    # Vector stores
    "VectorRecord": ("shadowbotagents.knowledge.vector_store", "VectorRecord"),
    "VectorStoreProtocol": ("shadowbotagents.knowledge.vector_store", "VectorStoreProtocol"),
    "VectorStoreRegistry": ("shadowbotagents.knowledge.vector_store", "VectorStoreRegistry"),
    "get_vector_store_registry": ("shadowbotagents.knowledge.vector_store", "get_vector_store_registry"),
    "InMemoryVectorStore": ("shadowbotagents.knowledge.vector_store", "InMemoryVectorStore"),
    
    # Retrieval
    "RetrievalResult": ("shadowbotagents.knowledge.retrieval", "RetrievalResult"),
    "RetrievalStrategy": ("shadowbotagents.knowledge.retrieval", "RetrievalStrategy"),
    "RetrieverProtocol": ("shadowbotagents.knowledge.retrieval", "RetrieverProtocol"),
    "RetrieverRegistry": ("shadowbotagents.knowledge.retrieval", "RetrieverRegistry"),
    "get_retriever_registry": ("shadowbotagents.knowledge.retrieval", "get_retriever_registry"),
    "reciprocal_rank_fusion": ("shadowbotagents.knowledge.retrieval", "reciprocal_rank_fusion"),
    "merge_adjacent_chunks": ("shadowbotagents.knowledge.retrieval", "merge_adjacent_chunks"),
    
    # Rerankers
    "RerankResult": ("shadowbotagents.knowledge.rerankers", "RerankResult"),
    "RerankerProtocol": ("shadowbotagents.knowledge.rerankers", "RerankerProtocol"),
    "RerankerRegistry": ("shadowbotagents.knowledge.rerankers", "RerankerRegistry"),
    "get_reranker_registry": ("shadowbotagents.knowledge.rerankers", "get_reranker_registry"),
    "SimpleReranker": ("shadowbotagents.knowledge.rerankers", "SimpleReranker"),
    
    # Index
    "IndexType": ("shadowbotagents.knowledge.index", "IndexType"),
    "IndexStats": ("shadowbotagents.knowledge.index", "IndexStats"),
    "IndexProtocol": ("shadowbotagents.knowledge.index", "IndexProtocol"),
    "IndexRegistry": ("shadowbotagents.knowledge.index", "IndexRegistry"),
    "get_index_registry": ("shadowbotagents.knowledge.index", "get_index_registry"),
    "KeywordIndex": ("shadowbotagents.knowledge.index", "KeywordIndex"),
    
    # Query engine
    "QueryMode": ("shadowbotagents.knowledge.query_engine", "QueryMode"),
    "QueryResult": ("shadowbotagents.knowledge.query_engine", "QueryResult"),
    "QueryEngineProtocol": ("shadowbotagents.knowledge.query_engine", "QueryEngineProtocol"),
    "QueryEngineRegistry": ("shadowbotagents.knowledge.query_engine", "QueryEngineRegistry"),
    "get_query_engine_registry": ("shadowbotagents.knowledge.query_engine", "get_query_engine_registry"),
    "decompose_question": ("shadowbotagents.knowledge.query_engine", "decompose_question"),
    "SimpleQueryEngine": ("shadowbotagents.knowledge.query_engine", "SimpleQueryEngine"),
    "SubQuestionEngine": ("shadowbotagents.knowledge.query_engine", "SubQuestionEngine"),
}


def __getattr__(name: str):
    """Lazy load protocols and registries."""
    if name in _LAZY_IMPORTS:
        module_path, attr_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(module_path)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """List available attributes."""
    return list(_LAZY_IMPORTS.keys()) + ["Knowledge", "Chunking"]


__all__ = [
    # Core
    "Knowledge",
    "Chunking",
    # Models and Protocols
    "SearchResultItem",
    "SearchResult",
    "AddResult",
    "normalize_search_item",
    "normalize_search_result",
    "normalize_to_dict",
    "KnowledgeStoreProtocol",
    "KnowledgeBackendError",
    "ScopeRequiredError",
    "BackendNotAvailableError",
    # Readers
    "Document",
    "ReaderProtocol",
    "ReaderRegistry",
    "get_reader_registry",
    "detect_source_kind",
    # Vector stores
    "VectorRecord",
    "VectorStoreProtocol",
    "VectorStoreRegistry",
    "get_vector_store_registry",
    "InMemoryVectorStore",
    # Retrieval
    "RetrievalResult",
    "RetrievalStrategy",
    "RetrieverProtocol",
    "RetrieverRegistry",
    "get_retriever_registry",
    "reciprocal_rank_fusion",
    "merge_adjacent_chunks",
    # Rerankers
    "RerankResult",
    "RerankerProtocol",
    "RerankerRegistry",
    "get_reranker_registry",
    "SimpleReranker",
    # Index
    "IndexType",
    "IndexStats",
    "IndexProtocol",
    "IndexRegistry",
    "get_index_registry",
    "KeywordIndex",
    # Query engine
    "QueryMode",
    "QueryResult",
    "QueryEngineProtocol",
    "QueryEngineRegistry",
    "get_query_engine_registry",
    "decompose_question",
    "SimpleQueryEngine",
    "SubQuestionEngine",
] 