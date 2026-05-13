"""Backward compatibility shim for shadowbotagents.push.client.

This module maintains backward compatibility for existing imports like:
    from shadowbotagents.push.client import PushClient

The actual implementation has been moved to the shadowbot wrapper package.
"""
from . import PushClient

__all__ = ["PushClient"]