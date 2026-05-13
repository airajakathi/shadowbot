"""Backward-compatible re-export. Prefer `shadowbot.scheduler`.

This module is deprecated. Use the canonical implementation in the
scheduler package for full functionality including YAML and recipe support.
"""

import warnings

warnings.warn(
    "shadowbot.agent_scheduler is deprecated; "
    "use 'from shadowbot.scheduler import AgentScheduler' instead.",
    DeprecationWarning, stacklevel=2,
)

from shadowbot.scheduler.agent_scheduler import (  # noqa: F401
    AgentScheduler, PraisonAgentExecutor, create_agent_scheduler
)
# Preserve the legacy public name as an alias of the canonical interface
from shadowbot.scheduler.base import ExecutorInterface as AgentExecutorInterface  # noqa: F401