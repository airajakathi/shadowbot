"""Agents module for managing multiple AI agents.

AgentTeam is the primary class for multi-agent coordination (v1.0+).
AgentManager, Agents, ShadowBotAgents are silent aliases for backward compatibility.
"""
from .agents import AgentTeam, AgentManager, Agents, ShadowBotAgents
from .autoagents import AutoAgents
from .auto_rag_agent import AutoRagAgent, AutoRagConfig, RetrievalPolicy
from .protocols import (
    MergeStrategyProtocol, FirstWinsMerge, ConcatMerge, DictMerge,
    TaskExecutorProtocol, ExecutionContext, TaskResult
)

__all__ = [
    'AgentTeam',  # Primary class (v1.0+)
    'AgentManager',  # Silent alias for AgentTeam
    'Agents',  # Silent alias for AgentTeam
    'ShadowBotAgents',  # Silent alias for AgentTeam
    'AutoAgents',
    'AutoRagAgent', 'AutoRagConfig', 'RetrievalPolicy',
    'MergeStrategyProtocol', 'FirstWinsMerge', 'ConcatMerge', 'DictMerge',
    'TaskExecutorProtocol', 'ExecutionContext', 'TaskResult',
]
