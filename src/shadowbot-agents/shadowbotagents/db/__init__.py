"""
Database adapter interface for ShadowBot Agents.

This module provides the protocol and types for database persistence.
Implementations are provided by the wrapper layer (shadowbot.db).

Usage (simplest - recommended):
    from shadowbotagents import Agent, db
    
    agent = Agent(
        name="Assistant",
        db=db(database_url="postgresql://localhost/mydb"),  # db(...) shortcut
        session_id="my-session"  # optional: defaults to per-hour ID
    )
    agent.chat("Hello!")  # auto-persists messages, runs, traces, tool calls

Alternative (explicit backend):
    db=db.DB(database_url="...")           # Short name (recommended)
    db=db.ShadowBotDB(database_url="...")  # Auto-detect backend
    db=db.PostgresDB(host="localhost")   # PostgreSQL
    db=db.SQLiteDB(path="data.db")       # SQLite
    db=db.RedisDB(host="localhost")      # Redis (state only)
"""

from .protocol import (
    DbAdapter,
    AsyncDbAdapter,
    DbMessage,
    DbToolCall,
    DbRun,
    DbSpan,
    DbTrace,
)


class _LazyDbModule:
    """
    Lazy proxy for database backends.
    
    Allows `from shadowbotagents import db` without importing heavy deps.
    Actual backend classes are loaded only when accessed.
    """
    
    _BACKENDS = {
        "DB": "shadowbot.db.adapter",  # recommended short name
        "ShadowBotDB": "shadowbot.db.adapter",
        "PraisonDB": "shadowbot.db.adapter",  # backward-compatible alias
        "PostgresDB": "shadowbot.db.adapter",
        "SQLiteDB": "shadowbot.db.adapter",
        "RedisDB": "shadowbot.db.adapter",
        "NeonDB": "shadowbot.db.adapter",
        "CockroachDB": "shadowbot.db.adapter",
        "XataDB": "shadowbot.db.adapter",
        "TursoDB": "shadowbot.db.adapter",
    }
    
    def __getattr__(self, name: str):
        if name in self._BACKENDS:
            try:
                import importlib
                module = importlib.import_module(self._BACKENDS[name])
                return getattr(module, name)
            except ImportError as e:
                raise ImportError(
                    f"Database backend '{name}' requires the shadowbot package. "
                    f"Install with: pip install shadowbot\n"
                    f"Original error: {e}"
                ) from e
        raise AttributeError(f"module 'db' has no attribute {name!r}")
    
    def __repr__(self):
        return "<module 'shadowbotagents.db' (lazy database backends)>"
    
    def __call__(self, **kwargs):
        """Shortcut: db(...) is equivalent to db.DB(...)"""
        return self.DB(**kwargs)


# Singleton lazy module instance
db = _LazyDbModule()


__all__ = [
    "DbAdapter",
    "AsyncDbAdapter",
    "DbMessage",
    "DbToolCall",
    "DbRun",
    "DbSpan",
    "DbTrace",
    "db",
]
