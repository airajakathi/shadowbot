"""
ShadowBot RAG - Retrieval Augmented Generation Module.

This module provides a thin orchestration layer over Knowledge for RAG workflows.
Knowledge handles indexing/retrieval; RAG adds answer generation with citations.

Usage:
    from shadowbotagents.rag import RAG, RAGConfig, RAGResult, Citation
    
    # With existing Knowledge
    rag = RAG(knowledge=my_knowledge)
    result = rag.query("What is the main finding?")
    print(result.answer)
    for citation in result.citations:
        print(f"  [{citation.id}] {citation.source}")

All imports are lazy to avoid performance impact when RAG is not used.
"""

from typing import TYPE_CHECKING

# Lazy loading to avoid import overhead
_LAZY_IMPORTS = {
    # Models
    "Citation": ("shadowbotagents.rag.models", "Citation"),
    "ContextPack": ("shadowbotagents.rag.models", "ContextPack"),
    "RAGResult": ("shadowbotagents.rag.models", "RAGResult"),
    "RAGConfig": ("shadowbotagents.rag.models", "RAGConfig"),
    # Unified retrieval config (Agent-first)
    "RetrievalConfig": ("shadowbotagents.rag.retrieval_config", "RetrievalConfig"),
    "RetrievalPolicy": ("shadowbotagents.rag.retrieval_config", "RetrievalPolicy"),
    "CitationsMode": ("shadowbotagents.rag.retrieval_config", "CitationsMode"),
    "create_retrieval_config": ("shadowbotagents.rag.retrieval_config", "create_retrieval_config"),
    # Token Budget (Phase 1)
    "TokenBudget": ("shadowbotagents.rag.budget", "TokenBudget"),
    "get_model_context_window": ("shadowbotagents.rag.budget", "get_model_context_window"),
    "BudgetEnforcerProtocol": ("shadowbotagents.rag.budget", "BudgetEnforcerProtocol"),
    "DefaultBudgetEnforcer": ("shadowbotagents.rag.budget", "DefaultBudgetEnforcer"),
    "estimate_tokens": ("shadowbotagents.rag.budget", "estimate_tokens"),
    # Strategy Selection (Phase 3) - RetrievalStrategy now from strategy module
    "RetrievalStrategy": ("shadowbotagents.rag.strategy", "RetrievalStrategy"),
    "select_strategy": ("shadowbotagents.rag.strategy", "select_strategy"),
    "get_strategy_description": ("shadowbotagents.rag.strategy", "get_strategy_description"),
    "STRATEGY_THRESHOLDS": ("shadowbotagents.rag.strategy", "STRATEGY_THRESHOLDS"),
    # SmartRetriever (Phase 4)
    "SmartRetriever": ("shadowbotagents.rag.retriever", "SmartRetriever"),
    "RetrievalResult": ("shadowbotagents.rag.retriever", "RetrievalResult"),
    "SimpleReranker": ("shadowbotagents.rag.retriever", "SimpleReranker"),
    "RetrieverProtocol": ("shadowbotagents.rag.retriever", "RetrieverProtocol"),
    "RerankerProtocol": ("shadowbotagents.rag.retriever", "RerankerProtocol"),
    # Compressor (Phase 5)
    "ContextCompressor": ("shadowbotagents.rag.compressor", "ContextCompressor"),
    "CompressionResult": ("shadowbotagents.rag.compressor", "CompressionResult"),
    "CompressorProtocol": ("shadowbotagents.rag.compressor", "CompressorProtocol"),
    # Summarizer (Phase 6)
    "HierarchicalSummarizer": ("shadowbotagents.rag.summarizer", "HierarchicalSummarizer"),
    "SummaryNode": ("shadowbotagents.rag.summarizer", "SummaryNode"),
    "HierarchyResult": ("shadowbotagents.rag.summarizer", "HierarchyResult"),
    # Protocols
    "ContextBuilderProtocol": ("shadowbotagents.rag.protocols", "ContextBuilderProtocol"),
    "CitationFormatterProtocol": ("shadowbotagents.rag.protocols", "CitationFormatterProtocol"),
    # Pipeline (internal - use Agent for primary access)
    "RAG": ("shadowbotagents.rag.pipeline", "RAG"),
    # Context utilities
    "build_context": ("shadowbotagents.rag.context", "build_context"),
    "truncate_context": ("shadowbotagents.rag.context", "truncate_context"),
    "deduplicate_chunks": ("shadowbotagents.rag.context", "deduplicate_chunks"),
}

import threading

_cache = {}
_cache_lock = threading.Lock()


def __getattr__(name: str):
    """Lazy load RAG components with thread safety."""
    if name in _cache:
        return _cache[name]
    
    if name in _LAZY_IMPORTS:
        with _cache_lock:
            # Double-check after acquiring lock
            if name in _cache:
                return _cache[name]
            module_path, attr_name = _LAZY_IMPORTS[name]
            import importlib
            module = importlib.import_module(module_path)
            value = getattr(module, attr_name)
            _cache[name] = value
            return value
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    """List available attributes."""
    return list(_LAZY_IMPORTS.keys())


__all__ = list(_LAZY_IMPORTS.keys())

if TYPE_CHECKING:
    from .models import Citation, ContextPack, RAGResult, RAGConfig
    from .protocols import ContextBuilderProtocol, CitationFormatterProtocol
    from .pipeline import RAG
    from .context import build_context, truncate_context, deduplicate_chunks
