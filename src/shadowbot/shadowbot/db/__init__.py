"""
ShadowBot Database - Ultra-simple persistence for agents.

RECOMMENDED (simplified import):
    from shadowbotagents import Agent, db
    # or: from shadowbot import Agent, db
    
    agent = Agent(
        name="Assistant",
        db=db(database_url="postgresql://localhost/mydb"),
        session_id="my-session"
    )
    agent.chat("Hello!")  # auto-persists + can resume

DEPRECATED (will be removed in v3.0):
    from shadowbot.db import PraisonDB  # Use db(...) instead

Supported backends:
- PostgreSQL, MySQL, SQLite (conversation)
- Qdrant, ChromaDB, Pinecone (knowledge/vector)
- Redis, Memory (state)
"""

import warnings

__all__ = [
    "DB",  # recommended short name
    "ShadowBotDB",
    "PraisonDB",  # backward-compatible alias
    "PostgresDB", 
    "SQLiteDB",
    "RedisDB",
    "NeonDB",
    "CockroachDB",
    "XataDB",
    "TursoDB",
]

# Deprecation warning message
_DEPRECATION_MSG = (
    "Importing from 'shadowbot.db' is deprecated and will be removed in v3.0. "
    "Use the simplified import instead:\n"
    "  from shadowbotagents import Agent, db\n"
    "  # or: from shadowbot import Agent, db\n"
    "Then use: db=db(database_url='...')"
)

# Lazy imports to avoid loading heavy dependencies
def __getattr__(name: str):
    if name == "DB":
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        from .adapter import DB
        return DB
    
    if name == "ShadowBotDB":
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        from .adapter import ShadowBotDB
        return ShadowBotDB
    
    if name == "PraisonDB":
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        from .adapter import PraisonDB
        return PraisonDB
    
    if name == "PostgresDB":
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        from .adapter import PostgresDB
        return PostgresDB
    
    if name == "SQLiteDB":
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        from .adapter import SQLiteDB
        return SQLiteDB
    
    if name == "RedisDB":
        warnings.warn(_DEPRECATION_MSG, DeprecationWarning, stacklevel=2)
        from .adapter import RedisDB
        return RedisDB
    
    if name == "NeonDB":
        from .adapter import NeonDB
        return NeonDB
    
    if name == "CockroachDB":
        from .adapter import CockroachDB
        return CockroachDB
    
    if name == "XataDB":
        from .adapter import XataDB
        return XataDB
    
    if name == "TursoDB":
        from .adapter import TursoDB
        return TursoDB
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
