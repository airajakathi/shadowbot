"""
AG-UI Protocol Integration for ShadowBot Agents

This module provides AG-UI (Agent-User Interface) protocol support,
enabling ShadowBot Agents to be exposed via a standardized streaming API
compatible with CopilotKit and other AG-UI frontends.

Usage:
    from shadowbotagents import Agent
    from shadowbotagents.ui.agui import AGUI
    from fastapi import FastAPI

    agent = Agent(name="Assistant", role="Helper", goal="Help users")
    agui = AGUI(agent=agent)

    app = FastAPI()
    app.include_router(agui.get_router())
"""

from shadowbotagents.ui.agui.agui import AGUI

__all__ = ["AGUI"]
