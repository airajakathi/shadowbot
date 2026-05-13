"""Backward compatibility shim for shadowbotagents.push.transports.

This module maintains backward compatibility for existing imports like:
    from shadowbotagents.push.transports import WebSocketTransport, PollingTransport

The actual implementations have been moved to the shadowbot wrapper package.
"""
from . import WebSocketTransport, PollingTransport

__all__ = ["WebSocketTransport", "PollingTransport"]