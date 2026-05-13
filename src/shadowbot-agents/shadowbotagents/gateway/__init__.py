"""
Gateway module for ShadowBot Agents.

Provides protocols and base classes for building gateway/control plane
implementations that coordinate multi-agent deployments.

This module contains only protocols and lightweight utilities.
Heavy implementations live in the shadowbot wrapper package.

Gap S2: WebSocketGateway is re-exported here for convenience but requires
the shadowbot wrapper package to be installed.
"""

from .protocols import (
    GatewayProtocol,
    GatewaySessionProtocol,
    GatewayClientProtocol,
    GatewayEvent,
    GatewayMessage,
    EventType,
    # Push protocols and dataclasses
    PushChannelProtocol,
    PresenceProtocol,
    DeliveryGuaranteeProtocol,
    ChannelInfo,
    PresenceInfo,
)
from .config import (
    GatewayConfig,
    SessionConfig,
    ChannelRouteConfig,
    MultiChannelGatewayConfig,
    # Push config
    PushConfig,
    RedisConfig,
    PresenceConfig,
    DeliveryConfig,
    PollingConfig,
)

# Lazy loading cache
_lazy_cache = {}


def __getattr__(name: str):
    """Lazy load heavy gateway implementations from shadowbot wrapper.
    
    Gap S2: Re-export WebSocketGateway from shadowbot wrapper for convenience.
    This allows downstream packages to import from shadowbotagents.gateway
    without needing to know about the shadowbot wrapper.
    """
    if name in _lazy_cache:
        return _lazy_cache[name]
    
    if name == "WebSocketGateway":
        try:
            from shadowbot.gateway import WebSocketGateway
            _lazy_cache[name] = WebSocketGateway
            return WebSocketGateway
        except ImportError:
            raise ImportError(
                "WebSocketGateway requires the shadowbot wrapper package. "
                "Install with: pip install shadowbot"
            )
    
    if name == "GatewaySession":
        try:
            from shadowbot.gateway import GatewaySession
            _lazy_cache[name] = GatewaySession
            return GatewaySession
        except ImportError:
            raise ImportError(
                "GatewaySession requires the shadowbot wrapper package. "
                "Install with: pip install shadowbot"
            )
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # Protocols (always available)
    "GatewayProtocol",
    "GatewaySessionProtocol",
    "GatewayClientProtocol",
    "GatewayEvent",
    "GatewayMessage",
    "EventType",
    # Push protocols (always available)
    "PushChannelProtocol",
    "PresenceProtocol",
    "DeliveryGuaranteeProtocol",
    "ChannelInfo",
    "PresenceInfo",
    # Config (always available)
    "GatewayConfig",
    "SessionConfig",
    "ChannelRouteConfig",
    "MultiChannelGatewayConfig",
    "PushConfig",
    "RedisConfig",
    "PresenceConfig",
    "DeliveryConfig",
    "PollingConfig",
    # Implementations (lazy loaded from shadowbot wrapper)
    "WebSocketGateway",
    "GatewaySession",
]
