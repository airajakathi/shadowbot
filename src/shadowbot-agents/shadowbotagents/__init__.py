"""
ShadowBot Agents - A package for hierarchical AI agent task execution

This module uses lazy loading to minimize import time and memory usage.
Heavy dependencies like litellm are only loaded when actually needed.
"""

# =============================================================================
# NAMING CONVENTION GUIDE (Simplified patterns for consistency)
# =============================================================================
# | Pattern       | When to Use             | Examples                        |
# |---------------|-------------------------|----------------------------------|
# | add_X         | Register something      | add_hook, add_tool, add_profile |
# | get_X         | Retrieve something      | get_tool, get_profile           |
# | remove_X      | Unregister something    | remove_hook, remove_tool        |
# | has_X         | Check existence         | has_hook, has_tool              |
# | list_X        | List all items          | list_tools, list_profiles       |
# | enable_X      | Turn on feature         | enable_telemetry                |
# | disable_X     | Turn off feature        | disable_telemetry               |
# | XConfig       | Configuration class     | MemoryConfig, HooksConfig       |
# | @decorator    | Decorator               | @tool, @add_hook                |
# |---------------|-------------------------|----------------------------------|
# | set_default_X | Internal/advanced only  | (don't simplify - internal)     |
# | create_X      | Factory function        | (already well-named)            |
# =============================================================================

# =============================================================================
# NAMESPACE PACKAGE GUARD
# =============================================================================
# Detect if we're loaded as a namespace package (which indicates stale artifacts
# in site-packages). This happens when there's a shadowbotagents/ directory in
# site-packages without an __init__.py file.
#
# Root cause: Partial uninstall or version mismatch leaves directories that
# Python's PathFinder treats as namespace packages, shadowing the real package.
# =============================================================================
if __file__ is None:
    import warnings as _ns_warnings
    _ns_warnings.warn(
        "shadowbotagents is loaded as a namespace package, which indicates "
        "stale artifacts in site-packages. This will cause import errors. "
        "Fix: Remove the stale directory with:\n"
        "  rm -rf $(python -c \"import site; print(site.getsitepackages()[0])\")/shadowbotagents/\n"
        "Then reinstall: pip install shadowbotagents",
        ImportWarning,
        stacklevel=1
    )
    del _ns_warnings

# Apply warning patch BEFORE any imports to intercept warnings at the source
from . import _warning_patch  # noqa: F401

# Import centralized logging configuration FIRST
from . import _logging

# Configure root logger after logging is initialized
_logging.configure_root_logger()

# Import configuration (lightweight, no heavy deps)
from . import _config

# Note: tools, config, memory, workflows, db, obs, knowledge and mcp are lazy-loaded via __getattr__ due to heavy deps

# Embedding API - LAZY LOADED via __getattr__ for performance
# Supports: embedding, embeddings, aembedding, aembeddings, EmbeddingResult, get_dimensions

# Workflows - LAZY LOADED (moved to __getattr__)
# Workflow, Task, WorkflowContext, StepResult, Route, Parallel, Loop, Repeat, etc.

# Guardrails - LAZY LOADED (imports main.py which imports rich)
# GuardrailResult and LLMGuardrail moved to __getattr__

# Handoff - LAZY LOADED (moved to __getattr__)
# Handoff, handoff, handoff_filters, etc.

# Flow display - LAZY LOADED (moved to __getattr__)
# FlowDisplay and track_workflow are now lazy loaded

# Main display utilities - LAZY LOADED to avoid importing rich at startup
# These are only needed when output=verbose, not for silent mode
# Moved to __getattr__ for lazy loading

# ============================================================================
# LAZY LOADING CONFIGURATION
# ============================================================================
# Using centralized _lazy.py utility for DRY, thread-safe lazy loading.
# All heavy dependencies are loaded on-demand to minimize import time.
# ============================================================================

from ._lazy import lazy_import, create_lazy_getattr_with_fallback

# Thread-safe cache for lazy-loaded values
_lazy_cache = {}

# Backward compatibility: _get_lazy_cache function for tests
import threading
_lazy_cache_local = threading.local()

def _get_lazy_cache():
    """Get thread-local lazy cache dict. Thread-safe for concurrent access.
    
    Note: This is kept for backward compatibility with tests.
    The main lazy loading now uses the centralized _lazy.py utility.
    """
    if not hasattr(_lazy_cache_local, 'cache'):
        _lazy_cache_local.cache = {}
    return _lazy_cache_local.cache

# ============================================================================
# LAZY IMPORT MAPPING
# ============================================================================
# Maps attribute names to (module_path, attr_name) tuples.
# This is the single source of truth for all lazy imports.
# ============================================================================

_LAZY_IMPORTS = {
    # Tools (moved from eager imports for lazy loading)
    'Tools': ('shadowbotagents.tools.tools', 'Tools'),
    'BaseTool': ('shadowbotagents.tools.base', 'BaseTool'),
    'ToolResult': ('shadowbotagents.tools.base', 'ToolResult'),
    'ToolValidationError': ('shadowbotagents.tools.base', 'ToolValidationError'),
    'validate_tool': ('shadowbotagents.tools.base', 'validate_tool'),
    'tool': ('shadowbotagents.tools.decorator', 'tool'),
    'FunctionTool': ('shadowbotagents.tools.decorator', 'FunctionTool'),
    'get_registry': ('shadowbotagents.tools.registry', 'get_registry'),
    'register_tool': ('shadowbotagents.tools.registry', 'register_tool'),
    'get_tool': ('shadowbotagents.tools.registry', 'get_tool'),
    'ToolRegistry': ('shadowbotagents.tools.registry', 'ToolRegistry'),
    
    # Main display utilities (imports rich)
    'TaskOutput': ('shadowbotagents.main', 'TaskOutput'),
    'ReflectionOutput': ('shadowbotagents.main', 'ReflectionOutput'),
    'display_interaction': ('shadowbotagents.main', 'display_interaction'),
    'display_self_reflection': ('shadowbotagents.main', 'display_self_reflection'),
    'display_instruction': ('shadowbotagents.main', 'display_instruction'),
    'display_tool_call': ('shadowbotagents.main', 'display_tool_call'),
    'display_error': ('shadowbotagents.main', 'display_error'),
    'display_generating': ('shadowbotagents.main', 'display_generating'),
    'clean_triple_backticks': ('shadowbotagents.main', 'clean_triple_backticks'),
    'error_logs': ('shadowbotagents.main', 'error_logs'),
    'register_display_callback': ('shadowbotagents.main', 'register_display_callback'),
    'sync_display_callbacks': ('shadowbotagents.main', 'sync_display_callbacks'),
    'async_display_callbacks': ('shadowbotagents.main', 'async_display_callbacks'),
    
    # AgentFlow (primary) / Workflow (alias)
    'AgentFlow': ('shadowbotagents.workflows', 'AgentFlow'),
    'Workflow': ('shadowbotagents.workflows', 'Workflow'),  # Silent alias
    'Pipeline': ('shadowbotagents.workflows', 'Pipeline'),  # Silent alias
    'WorkflowContext': ('shadowbotagents.workflows', 'WorkflowContext'),
    'StepResult': ('shadowbotagents.workflows', 'StepResult'),
    'Route': ('shadowbotagents.workflows', 'Route'),
    'Parallel': ('shadowbotagents.workflows', 'Parallel'),
    'Loop': ('shadowbotagents.workflows', 'Loop'),
    'Repeat': ('shadowbotagents.workflows', 'Repeat'),
    'If': ('shadowbotagents.workflows', 'If'),
    'route': ('shadowbotagents.workflows', 'route'),
    'parallel': ('shadowbotagents.workflows', 'parallel'),
    'loop': ('shadowbotagents.workflows', 'loop'),
    'repeat': ('shadowbotagents.workflows', 'repeat'),
    'when': ('shadowbotagents.workflows', 'when'),
    
    # Conditions (Protocol-driven condition evaluation)
    'ConditionProtocol': ('shadowbotagents.conditions.protocols', 'ConditionProtocol'),
    'RoutingConditionProtocol': ('shadowbotagents.conditions.protocols', 'RoutingConditionProtocol'),
    'ExpressionCondition': ('shadowbotagents.conditions.evaluator', 'ExpressionCondition'),
    'DictCondition': ('shadowbotagents.conditions.evaluator', 'DictCondition'),
    'evaluate_condition': ('shadowbotagents.conditions.evaluator', 'evaluate_condition'),
    
    # Handoff
    'Handoff': ('shadowbotagents.agent.handoff', 'Handoff'),
    'handoff': ('shadowbotagents.agent.handoff', 'handoff'),
    'handoff_filters': ('shadowbotagents.agent.handoff', 'handoff_filters'),
    'parallel_handoffs': ('shadowbotagents.agent.handoff', 'parallel_handoffs'),
    'RECOMMENDED_PROMPT_PREFIX': ('shadowbotagents.agent.handoff', 'RECOMMENDED_PROMPT_PREFIX'),
    'prompt_with_handoff_instructions': ('shadowbotagents.agent.handoff', 'prompt_with_handoff_instructions'),
    'HandoffConfig': ('shadowbotagents.agent.handoff', 'HandoffConfig'),
    'HandoffResult': ('shadowbotagents.agent.handoff', 'HandoffResult'),
    'HandoffInputData': ('shadowbotagents.agent.handoff', 'HandoffInputData'),
    'ContextPolicy': ('shadowbotagents.agent.handoff', 'ContextPolicy'),
    'HandoffError': ('shadowbotagents.errors', 'HandoffError'),
    'HandoffCycleError': ('shadowbotagents.errors', 'HandoffCycleError'),
    'HandoffDepthError': ('shadowbotagents.errors', 'HandoffDepthError'),
    'HandoffTimeoutError': ('shadowbotagents.errors', 'HandoffTimeoutError'),
    
    # Embedding API (Note: embedding/embeddings handled in custom_handler to override subpackage)
    'aembedding': ('shadowbotagents.embedding.embed', 'aembedding'),
    'aembeddings': ('shadowbotagents.embedding.embed', 'aembedding'),
    'embed': ('shadowbotagents.embedding.embed', 'embed'),
    'aembed': ('shadowbotagents.embedding.embed', 'aembed'),
    'EmbeddingResult': ('shadowbotagents.embedding.result', 'EmbeddingResult'),
    'get_dimensions': ('shadowbotagents.embedding.dimensions', 'get_dimensions'),
    
    # Guardrails
    'GuardrailResult': ('shadowbotagents.guardrails', 'GuardrailResult'),
    'LLMGuardrail': ('shadowbotagents.guardrails', 'LLMGuardrail'),
    
    # Approval (agent-centric approval backends)
    'AutoApproveBackend': ('shadowbotagents.approval.backends', 'AutoApproveBackend'),
    'ConsoleBackend': ('shadowbotagents.approval.backends', 'ConsoleBackend'),
    
    # Flow display
    'FlowDisplay': ('shadowbotagents.flow_display', 'FlowDisplay'),
    'track_workflow': ('shadowbotagents.flow_display', 'track_workflow'),
    
    # CLI Backend Protocol (Protocol-driven external CLI integration)
    'CliBackendProtocol': ('shadowbotagents.cli_backend.protocols', 'CliBackendProtocol'),
    'CliBackendConfig': ('shadowbotagents.cli_backend.protocols', 'CliBackendConfig'),
    'CliSessionBinding': ('shadowbotagents.cli_backend.protocols', 'CliSessionBinding'),
    'CliBackendResult': ('shadowbotagents.cli_backend.protocols', 'CliBackendResult'),
    'CliBackendDelta': ('shadowbotagents.cli_backend.protocols', 'CliBackendDelta'),
    
    # Agent classes
    'Agent': ('shadowbotagents.agent.agent', 'Agent'),
    'BudgetExceededError': ('shadowbotagents.errors', 'BudgetExceededError'),
    
    # Error hierarchy - structured exception handling
    'ShadowBotError': ('shadowbotagents.errors', 'ShadowBotError'),
    'ToolExecutionError': ('shadowbotagents.errors', 'ToolExecutionError'),
    'LLMError': ('shadowbotagents.errors', 'LLMError'),
    'ValidationError': ('shadowbotagents.errors', 'ValidationError'),
    'NetworkError': ('shadowbotagents.errors', 'NetworkError'),
    'ShadowBotConfigError': ('shadowbotagents.errors', 'ShadowBotConfigError'),
    'ErrorContextProtocol': ('shadowbotagents.errors', 'ErrorContextProtocol'),
    'Heartbeat': ('shadowbotagents.agent.heartbeat', 'Heartbeat'),
    'HeartbeatConfig': ('shadowbotagents.agent.heartbeat', 'HeartbeatConfig'),
    'ImageAgent': ('shadowbotagents.agent.image_agent', 'ImageAgent'),
    'VideoAgent': ('shadowbotagents.agent.video_agent', 'VideoAgent'),
    'VideoConfig': ('shadowbotagents.agent.video_agent', 'VideoConfig'),
    'AudioAgent': ('shadowbotagents.agent.audio_agent', 'AudioAgent'),
    'AudioConfig': ('shadowbotagents.agent.audio_agent', 'AudioConfig'),
    'OCRAgent': ('shadowbotagents.agent.ocr_agent', 'OCRAgent'),
    'OCRConfig': ('shadowbotagents.agent.ocr_agent', 'OCRConfig'),
    'ContextAgent': ('shadowbotagents.agent.context_agent', 'ContextAgent'),
    'create_context_agent': ('shadowbotagents.agent.context_agent', 'create_context_agent'),
    'DeepResearchAgent': ('shadowbotagents.agent.deep_research_agent', 'DeepResearchAgent'),
    'DeepResearchResponse': ('shadowbotagents.agent.deep_research_agent', 'DeepResearchResponse'),
    'ReasoningStep': ('shadowbotagents.agent.deep_research_agent', 'ReasoningStep'),
    'WebSearchCall': ('shadowbotagents.agent.deep_research_agent', 'WebSearchCall'),
    'CodeExecutionStep': ('shadowbotagents.agent.deep_research_agent', 'CodeExecutionStep'),
    'MCPCall': ('shadowbotagents.agent.deep_research_agent', 'MCPCall'),
    'FileSearchCall': ('shadowbotagents.agent.deep_research_agent', 'FileSearchCall'),
    'Provider': ('shadowbotagents.agent.deep_research_agent', 'Provider'),
    'QueryRewriterAgent': ('shadowbotagents.agent.query_rewriter_agent', 'QueryRewriterAgent'),
    'RewriteStrategy': ('shadowbotagents.agent.query_rewriter_agent', 'RewriteStrategy'),
    'RewriteResult': ('shadowbotagents.agent.query_rewriter_agent', 'RewriteResult'),
    'PromptExpanderAgent': ('shadowbotagents.agent.prompt_expander_agent', 'PromptExpanderAgent'),
    'ExpandStrategy': ('shadowbotagents.agent.prompt_expander_agent', 'ExpandStrategy'),
    'ExpandResult': ('shadowbotagents.agent.prompt_expander_agent', 'ExpandResult'),
    'VisionAgent': ('shadowbotagents.agent.vision_agent', 'VisionAgent'),
    'VisionConfig': ('shadowbotagents.agent.vision_agent', 'VisionConfig'),
    'EmbeddingAgent': ('shadowbotagents.agent.embedding_agent', 'EmbeddingAgent'),
    'EmbeddingConfig': ('shadowbotagents.agent.embedding_agent', 'EmbeddingConfig'),
    'RealtimeAgent': ('shadowbotagents.agent.realtime_agent', 'RealtimeAgent'),
    'RealtimeConfig': ('shadowbotagents.agent.realtime_agent', 'RealtimeConfig'),
    'CodeAgent': ('shadowbotagents.agent.code_agent', 'CodeAgent'),
    'CodeConfig': ('shadowbotagents.agent.code_agent', 'CodeConfig'),
    
    # AgentTeam (primary) / AgentManager (alias)
    'AgentTeam': ('shadowbotagents.agents.agents', 'AgentTeam'),
    'AgentManager': ('shadowbotagents.agents.agents', 'AgentManager'),  # Silent alias
    # Note: 'Agents' is handled by _custom_handler for deprecation warning
    'Task': ('shadowbotagents.task.task', 'Task'),
    'AutoAgents': ('shadowbotagents.agents.autoagents', 'AutoAgents'),
    'AutoRagAgent': ('shadowbotagents.agents.auto_rag_agent', 'AutoRagAgent'),
    'AutoRagConfig': ('shadowbotagents.agents.auto_rag_agent', 'AutoRagConfig'),
    'RagRetrievalPolicy': ('shadowbotagents.agents.auto_rag_agent', 'RetrievalPolicy'),
    
    # Session
    'Session': ('shadowbotagents.session', 'Session'),
    
    # AgentOS (primary) / AgentApp (alias) - protocol and config
    'AgentOSProtocol': ('shadowbotagents.app.protocols', 'AgentOSProtocol'),
    'AgentOSConfig': ('shadowbotagents.app', 'AgentOSConfig'),
    'AgentAppProtocol': ('shadowbotagents.app.protocols', 'AgentAppProtocol'),  # Silent alias
    'AgentAppConfig': ('shadowbotagents.app.config', 'AgentAppConfig'),  # Silent alias
    
    # MCP (optional)
    'MCP': ('shadowbotagents.mcp.mcp', 'MCP'),
    
    # Knowledge
    'Knowledge': ('shadowbotagents.knowledge.knowledge', 'Knowledge'),
    'Chunking': ('shadowbotagents.knowledge.chunking', 'Chunking'),
    
    # FastContext
    'FastContext': ('shadowbotagents.context.fast', 'FastContext'),
    'FastContextResult': ('shadowbotagents.context.fast', 'FastContextResult'),
    'FileMatch': ('shadowbotagents.context.fast', 'FileMatch'),
    'LineRange': ('shadowbotagents.context.fast', 'LineRange'),
    
    # RAG
    'RetrievalConfig': ('shadowbotagents.rag.retrieval_config', 'RetrievalConfig'),
    'RetrievalPolicy': ('shadowbotagents.rag.retrieval_config', 'RetrievalPolicy'),
    'CitationsMode': ('shadowbotagents.rag.retrieval_config', 'CitationsMode'),
    'ContextPack': ('shadowbotagents.rag.models', 'ContextPack'),
    'RAGResult': ('shadowbotagents.rag', 'RAGResult'),
    'Citation': ('shadowbotagents.rag', 'Citation'),
    'RAG': ('shadowbotagents.rag', 'RAG'),
    'RAGConfig': ('shadowbotagents.rag', 'RAGConfig'),
    'RAGCitation': ('shadowbotagents.rag', 'Citation'),
    
    # Skills
    'SkillManager': ('shadowbotagents.skills', 'SkillManager'),
    'SkillProperties': ('shadowbotagents.skills', 'SkillProperties'),
    'SkillMetadata': ('shadowbotagents.skills', 'SkillMetadata'),
    'SkillLoader': ('shadowbotagents.skills', 'SkillLoader'),
    
    # Memory
    'Memory': ('shadowbotagents.memory.memory', 'Memory'),
    
    # Planning
    'Plan': ('shadowbotagents.planning', 'Plan'),
    'PlanStep': ('shadowbotagents.planning', 'PlanStep'),
    'TodoList': ('shadowbotagents.planning', 'TodoList'),
    'TodoItem': ('shadowbotagents.planning', 'TodoItem'),
    'PlanStorage': ('shadowbotagents.planning', 'PlanStorage'),
    'PlanningAgent': ('shadowbotagents.planning', 'PlanningAgent'),
    'ApprovalCallback': ('shadowbotagents.planning', 'ApprovalCallback'),
    'READ_ONLY_TOOLS': ('shadowbotagents.planning', 'READ_ONLY_TOOLS'),
    'RESTRICTED_TOOLS': ('shadowbotagents.planning', 'RESTRICTED_TOOLS'),
    
    # Trace (protocol-driven, for custom sinks) - AGENTS.md naming: XProtocol
    'ContextTraceSinkProtocol': ('shadowbotagents.trace', 'ContextTraceSinkProtocol'),
    'ContextTraceSink': ('shadowbotagents.trace', 'ContextTraceSink'),  # Backward compat alias
    'TraceSinkProtocol': ('shadowbotagents.trace', 'TraceSinkProtocol'),
    'TraceSink': ('shadowbotagents.trace', 'TraceSink'),  # Backward compat alias
    'ContextTraceEmitter': ('shadowbotagents.trace', 'ContextTraceEmitter'),
    'ContextEvent': ('shadowbotagents.trace', 'ContextEvent'),
    'ContextEventType': ('shadowbotagents.trace', 'ContextEventType'),
    'trace_context': ('shadowbotagents.trace', 'trace_context'),
    'ContextListSink': ('shadowbotagents.trace', 'ContextListSink'),
    'ContextNoOpSink': ('shadowbotagents.trace', 'ContextNoOpSink'),
    
    # Telemetry
    'get_telemetry': ('shadowbotagents.telemetry', 'get_telemetry'),
    'enable_telemetry': ('shadowbotagents.telemetry', 'enable_telemetry'),
    'disable_telemetry': ('shadowbotagents.telemetry', 'disable_telemetry'),
    'enable_performance_mode': ('shadowbotagents.telemetry', 'enable_performance_mode'),
    'disable_performance_mode': ('shadowbotagents.telemetry', 'disable_performance_mode'),
    'cleanup_telemetry_resources': ('shadowbotagents.telemetry', 'cleanup_telemetry_resources'),
    'MinimalTelemetry': ('shadowbotagents.telemetry', 'MinimalTelemetry'),
    'TelemetryCollector': ('shadowbotagents.telemetry', 'TelemetryCollector'),
    
    # UI (optional)
    'AGUI': ('shadowbotagents.ui.agui', 'AGUI'),
    'A2A': ('shadowbotagents.ui.a2a', 'A2A'),
    
    # Feature configs
    'MemoryConfig': ('shadowbotagents.config.feature_configs', 'MemoryConfig'),
    'KnowledgeConfig': ('shadowbotagents.config.feature_configs', 'KnowledgeConfig'),
    'PlanningConfig': ('shadowbotagents.config.feature_configs', 'PlanningConfig'),
    'ReflectionConfig': ('shadowbotagents.config.feature_configs', 'ReflectionConfig'),
    'GuardrailConfig': ('shadowbotagents.config.feature_configs', 'GuardrailConfig'),
    'WebConfig': ('shadowbotagents.config.feature_configs', 'WebConfig'),
    'OutputConfig': ('shadowbotagents.config.feature_configs', 'OutputConfig'),
    'ExecutionConfig': ('shadowbotagents.config.feature_configs', 'ExecutionConfig'),
    'TemplateConfig': ('shadowbotagents.config.feature_configs', 'TemplateConfig'),
    'CachingConfig': ('shadowbotagents.config.feature_configs', 'CachingConfig'),
    'HooksConfig': ('shadowbotagents.config.feature_configs', 'HooksConfig'),
    'SkillsConfig': ('shadowbotagents.config.feature_configs', 'SkillsConfig'),
    'AutonomyConfig': ('shadowbotagents.agent.autonomy', 'AutonomyConfig'),
    'EscalationStage': ('shadowbotagents.escalation.types', 'EscalationStage'),
    'EscalationPipeline': ('shadowbotagents.escalation.pipeline', 'EscalationPipeline'),
    'ObservabilityHooks': ('shadowbotagents.escalation.observability', 'ObservabilityHooks'),
    'ObservabilityEventType': ('shadowbotagents.escalation.observability', 'EventType'),
    'DoomLoopDetector': ('shadowbotagents.escalation.doom_loop', 'DoomLoopDetector'),
    'MemoryBackend': ('shadowbotagents.config.feature_configs', 'MemoryBackend'),
    'LearnConfig': ('shadowbotagents.config.feature_configs', 'LearnConfig'),
    'LearnScope': ('shadowbotagents.config.feature_configs', 'LearnScope'),
    'LearnMode': ('shadowbotagents.config.feature_configs', 'LearnMode'),
    'LearnBackend': ('shadowbotagents.config.feature_configs', 'LearnBackend'),
    'LearnProtocol': ('shadowbotagents.memory.learn.protocols', 'LearnProtocol'),
    'AsyncLearnProtocol': ('shadowbotagents.memory.learn.protocols', 'AsyncLearnProtocol'),
    'LearnManagerProtocol': ('shadowbotagents.memory.learn.protocols', 'LearnManagerProtocol'),
    'LearnManager': ('shadowbotagents.memory.learn', 'LearnManager'),
    'ChunkingStrategy': ('shadowbotagents.config.feature_configs', 'ChunkingStrategy'),
    'GuardrailAction': ('shadowbotagents.config.feature_configs', 'GuardrailAction'),
    'WebSearchProvider': ('shadowbotagents.config.feature_configs', 'WebSearchProvider'),
    'OutputPreset': ('shadowbotagents.config.feature_configs', 'OutputPreset'),
    'ExecutionPreset': ('shadowbotagents.config.feature_configs', 'ExecutionPreset'),
    'AutonomyLevel': ('shadowbotagents.config.feature_configs', 'AutonomyLevel'),
    'MultiAgentHooksConfig': ('shadowbotagents.config.feature_configs', 'MultiAgentHooksConfig'),
    'MultiAgentOutputConfig': ('shadowbotagents.config.feature_configs', 'MultiAgentOutputConfig'),
    'MultiAgentExecutionConfig': ('shadowbotagents.config.feature_configs', 'MultiAgentExecutionConfig'),
    'MultiAgentPlanningConfig': ('shadowbotagents.config.feature_configs', 'MultiAgentPlanningConfig'),
    'MultiAgentMemoryConfig': ('shadowbotagents.config.feature_configs', 'MultiAgentMemoryConfig'),
    
    # Parameter resolver
    'resolve': ('shadowbotagents.config.param_resolver', 'resolve'),
    'ArrayMode': ('shadowbotagents.config.param_resolver', 'ArrayMode'),
    'resolve_memory': ('shadowbotagents.config.param_resolver', 'resolve_memory'),
    'resolve_knowledge': ('shadowbotagents.config.param_resolver', 'resolve_knowledge'),
    'resolve_output': ('shadowbotagents.config.param_resolver', 'resolve_output'),
    'resolve_execution': ('shadowbotagents.config.param_resolver', 'resolve_execution'),
    'resolve_web': ('shadowbotagents.config.param_resolver', 'resolve_web'),
    'resolve_planning': ('shadowbotagents.config.param_resolver', 'resolve_planning'),
    'resolve_reflection': ('shadowbotagents.config.param_resolver', 'resolve_reflection'),
    'resolve_context': ('shadowbotagents.config.param_resolver', 'resolve_context'),
    'resolve_autonomy': ('shadowbotagents.config.param_resolver', 'resolve_autonomy'),
    'resolve_caching': ('shadowbotagents.config.param_resolver', 'resolve_caching'),
    'resolve_hooks': ('shadowbotagents.config.param_resolver', 'resolve_hooks'),
    'resolve_skills': ('shadowbotagents.config.param_resolver', 'resolve_skills'),
    'resolve_routing': ('shadowbotagents.config.param_resolver', 'resolve_routing'),
    'resolve_guardrails': ('shadowbotagents.config.param_resolver', 'resolve_guardrails'),
    'resolve_guardrail_policies': ('shadowbotagents.config.param_resolver', 'resolve_guardrail_policies'),
    
    # Presets
    'MEMORY_PRESETS': ('shadowbotagents.config.presets', 'MEMORY_PRESETS'),
    'MEMORY_URL_SCHEMES': ('shadowbotagents.config.presets', 'MEMORY_URL_SCHEMES'),
    'OUTPUT_PRESETS': ('shadowbotagents.config.presets', 'OUTPUT_PRESETS'),
    'EXECUTION_PRESETS': ('shadowbotagents.config.presets', 'EXECUTION_PRESETS'),
    'WEB_PRESETS': ('shadowbotagents.config.presets', 'WEB_PRESETS'),
    'PLANNING_PRESETS': ('shadowbotagents.config.presets', 'PLANNING_PRESETS'),
    'REFLECTION_PRESETS': ('shadowbotagents.config.presets', 'REFLECTION_PRESETS'),
    'CONTEXT_PRESETS': ('shadowbotagents.config.presets', 'CONTEXT_PRESETS'),
    'AUTONOMY_PRESETS': ('shadowbotagents.config.presets', 'AUTONOMY_PRESETS'),
    'CACHING_PRESETS': ('shadowbotagents.config.presets', 'CACHING_PRESETS'),
    'MULTI_AGENT_OUTPUT_PRESETS': ('shadowbotagents.config.presets', 'MULTI_AGENT_OUTPUT_PRESETS'),
    'MULTI_AGENT_EXECUTION_PRESETS': ('shadowbotagents.config.presets', 'MULTI_AGENT_EXECUTION_PRESETS'),
    'GUARDRAIL_PRESETS': ('shadowbotagents.config.presets', 'GUARDRAIL_PRESETS'),
    'KNOWLEDGE_PRESETS': ('shadowbotagents.config.presets', 'KNOWLEDGE_PRESETS'),
    
    # Parse utilities
    'detect_url_scheme': ('shadowbotagents.config.parse_utils', 'detect_url_scheme'),
    'is_path_like': ('shadowbotagents.config.parse_utils', 'is_path_like'),
    'suggest_similar': ('shadowbotagents.config.parse_utils', 'suggest_similar'),
    'is_policy_string': ('shadowbotagents.config.parse_utils', 'is_policy_string'),
    'parse_policy_string': ('shadowbotagents.config.parse_utils', 'parse_policy_string'),
    
    # Context management
    'ContextConfig': ('shadowbotagents.context.models', 'ContextConfig'),
    'OptimizerStrategy': ('shadowbotagents.context.models', 'OptimizerStrategy'),
    'ManagerConfig': ('shadowbotagents.context.manager', 'ManagerConfig'),
    'ContextManager': ('shadowbotagents.context.manager', 'ContextManager'),
    
    # db module
    'db': ('shadowbotagents.db', 'db'),
    # Note: 'obs' is handled by custom_handler to return _LazyObsModule instance
    
    # Gateway protocols and config (implementations in shadowbot wrapper)
    'GatewayProtocol': ('shadowbotagents.gateway.protocols', 'GatewayProtocol'),
    'GatewaySessionProtocol': ('shadowbotagents.gateway.protocols', 'GatewaySessionProtocol'),
    'GatewayClientProtocol': ('shadowbotagents.gateway.protocols', 'GatewayClientProtocol'),
    'GatewayEvent': ('shadowbotagents.gateway.protocols', 'GatewayEvent'),
    'GatewayMessage': ('shadowbotagents.gateway.protocols', 'GatewayMessage'),
    'EventType': ('shadowbotagents.gateway.protocols', 'EventType'),
    'GatewayConfig': ('shadowbotagents.gateway.config', 'GatewayConfig'),
    'SessionConfig': ('shadowbotagents.gateway.config', 'SessionConfig'),
    
    # Bot protocols and config (implementations in shadowbot wrapper)
    'BotProtocol': ('shadowbotagents.bots.protocols', 'BotProtocol'),
    'BotMessage': ('shadowbotagents.bots.protocols', 'BotMessage'),
    'BotUser': ('shadowbotagents.bots.protocols', 'BotUser'),
    'BotChannel': ('shadowbotagents.bots.protocols', 'BotChannel'),
    'MessageType': ('shadowbotagents.bots.protocols', 'MessageType'),
    'BotConfig': ('shadowbotagents.bots.config', 'BotConfig'),
    'BotOSProtocol': ('shadowbotagents.bots.protocols', 'BotOSProtocol'),
    'BotOSConfig': ('shadowbotagents.bots.config', 'BotOSConfig'),
    
    # Sandbox protocols and config (implementations in shadowbot wrapper)
    'SandboxProtocol': ('shadowbotagents.sandbox.protocols', 'SandboxProtocol'),
    'SandboxResult': ('shadowbotagents.sandbox.protocols', 'SandboxResult'),
    'SandboxStatus': ('shadowbotagents.sandbox.protocols', 'SandboxStatus'),
    'ResourceLimits': ('shadowbotagents.sandbox.protocols', 'ResourceLimits'),
    'SandboxConfig': ('shadowbotagents.sandbox.config', 'SandboxConfig'),
    'SecurityPolicy': ('shadowbotagents.sandbox.config', 'SecurityPolicy'),
    
    # Managed backend protocol (implementation + config in shadowbot wrapper)
    'ManagedBackendProtocol': ('shadowbotagents.agent.protocols', 'ManagedBackendProtocol'),
    
    # Managed agent events (provider-agnostic)
    'ManagedEvent': ('shadowbotagents.managed.events', 'ManagedEvent'),
    'AgentMessageEvent': ('shadowbotagents.managed.events', 'AgentMessageEvent'),
    'ToolUseEvent': ('shadowbotagents.managed.events', 'ToolUseEvent'),
    'CustomToolUseEvent': ('shadowbotagents.managed.events', 'CustomToolUseEvent'),
    'SessionIdleEvent': ('shadowbotagents.managed.events', 'SessionIdleEvent'),
    'SessionErrorEvent': ('shadowbotagents.managed.events', 'SessionErrorEvent'),
    'EventType': ('shadowbotagents.managed.events', 'EventType'),
    'StopReason': ('shadowbotagents.managed.events', 'StopReason'),
    
    # Model failover
    'AuthProfile': ('shadowbotagents.llm.failover', 'AuthProfile'),
    'ProviderStatus': ('shadowbotagents.llm.failover', 'ProviderStatus'),
    'FailoverConfig': ('shadowbotagents.llm.failover', 'FailoverConfig'),
    'FailoverManager': ('shadowbotagents.llm.failover', 'FailoverManager'),
    
    # Plugins - Core classes
    'PluginManager': ('shadowbotagents.plugins', 'PluginManager'),
    'Plugin': ('shadowbotagents.plugins', 'Plugin'),
    'PluginInfo': ('shadowbotagents.plugins', 'PluginInfo'),
    'PluginHook': ('shadowbotagents.plugins', 'PluginHook'),
    'FunctionPlugin': ('shadowbotagents.plugins', 'FunctionPlugin'),
    'get_plugin_manager': ('shadowbotagents.plugins', 'get_plugin_manager'),
    
    # Plugins - Protocols
    'PluginProtocol': ('shadowbotagents.plugins', 'PluginProtocol'),
    'ToolPluginProtocol': ('shadowbotagents.plugins', 'ToolPluginProtocol'),
    'HookPluginProtocol': ('shadowbotagents.plugins', 'HookPluginProtocol'),
    'AgentPluginProtocol': ('shadowbotagents.plugins', 'AgentPluginProtocol'),
    'LLMPluginProtocol': ('shadowbotagents.plugins', 'LLMPluginProtocol'),
    
    # Plugins - Single-file plugin support
    'PluginMetadata': ('shadowbotagents.plugins', 'PluginMetadata'),
    'PluginParseError': ('shadowbotagents.plugins', 'PluginParseError'),
    'parse_plugin_header': ('shadowbotagents.plugins', 'parse_plugin_header'),
    'parse_plugin_header_from_file': ('shadowbotagents.plugins', 'parse_plugin_header_from_file'),
    'discover_plugins': ('shadowbotagents.plugins', 'discover_plugins'),
    'load_plugin': ('shadowbotagents.plugins', 'load_plugin'),
    'discover_and_load_plugins': ('shadowbotagents.plugins', 'discover_and_load_plugins'),
    'get_default_plugin_dirs': ('shadowbotagents.plugins', 'get_default_plugin_dirs'),
    'get_plugin_template': ('shadowbotagents.plugins', 'get_plugin_template'),
    'ensure_plugin_dir': ('shadowbotagents.plugins', 'ensure_plugin_dir'),
    
    # Config loader - for config-driven defaults
    'get_config': ('shadowbotagents.config.loader', 'get_config'),
    'get_default': ('shadowbotagents.config.loader', 'get_default'),
    'get_plugins_config': ('shadowbotagents.config.loader', 'get_plugins_config'),
    'get_defaults_config': ('shadowbotagents.config.loader', 'get_defaults_config'),
    'apply_config_defaults': ('shadowbotagents.config.loader', 'apply_config_defaults'),
    'validate_config': ('shadowbotagents.config.loader', 'validate_config'),
    'get_config_path': ('shadowbotagents.config.loader', 'get_config_path'),
    'ConfigValidationError': ('shadowbotagents.config.loader', 'ConfigValidationError'),
    'PraisonConfig': ('shadowbotagents.config.loader', 'PraisonConfig'),
    'PluginsConfig': ('shadowbotagents.config.loader', 'PluginsConfig'),
    'DefaultsConfig': ('shadowbotagents.config.loader', 'DefaultsConfig'),
    
    # Centralized Logging Utilities
    'get_logger': ('shadowbotagents._logging', 'get_logger'),
    'configure_structured_logging': ('shadowbotagents._logging', 'configure_structured_logging'),
    'StructuredFormatter': ('shadowbotagents._logging', 'StructuredFormatter'),
}

# ============================================================================
# SUBPACKAGE FUNCTION OVERRIDES
# ============================================================================
# Some subpackage names conflict with function names we want to export.
# Override them here to return the function instead of the module.
# ============================================================================

# Override 'embedding' and 'embeddings' at module level to prevent subpackage import
# These need to be set after _LAZY_IMPORTS is defined but before __getattr__ is created
def _get_embedding_func():
    """Lazy getter for embedding function."""
    # Import with alias to avoid overwriting the module proxy
    from .embedding.embed import embedding as _embedding_func
    return _embedding_func

# Create lazy properties that override the submodule
class _EmbeddingProxy:
    """Proxy object that loads embedding function on first access."""
    def __init__(self):
        self._func = None
    
    def _load(self):
        """Load the actual embedding function if not already loaded."""
        if self._func is None:
            self._func = _get_embedding_func()
        return self._func
    
    def __call__(self, *args, **kwargs):
        return self._load()(*args, **kwargs)
    
    def __getattr__(self, name):
        return getattr(self._load(), name)
    
    @property
    def __wrapped__(self):
        """Support for inspect.signature() and functools.wraps."""
        return self._load()
    
    @property
    def __signature__(self):
        """Support for inspect.signature()."""
        import inspect
        return inspect.signature(self._load())
    
    def __repr__(self):
        return f"<lazy proxy for {self._load()!r}>"

_global_embedding_proxy = _EmbeddingProxy()

def _custom_handler(name, cache):
    """Handle special cases that need custom logic."""
    import warnings
    
    # Agents is a silent alias for AgentManager
    if name == "Agents":
        value = lazy_import('shadowbotagents.agents.agents', 'AgentManager', cache)
        cache['AgentManager'] = value
        cache['Agents'] = value
        return value
        
    # Handle embedding specifically if missing from module dict due to submodule reload
    if name in ("embedding", "embeddings"):
        return _global_embedding_proxy
    
    # Module imports (return the module itself)
    if name == 'tools':
        import importlib
        mod = importlib.import_module('.tools', 'shadowbotagents')
        cache['tools'] = mod
        return mod
    if name == 'config':
        import importlib
        mod = importlib.import_module('.config', 'shadowbotagents')
        cache['config'] = mod
        return mod
    if name == 'memory':
        import importlib
        mod = importlib.import_module('.memory', 'shadowbotagents')
        cache['memory'] = mod
        return mod
    if name == 'workflows':
        import importlib
        mod = importlib.import_module('.workflows', 'shadowbotagents')
        cache['workflows'] = mod
        return mod
    if name == 'obs':
        import importlib
        mod = importlib.import_module('.obs', 'shadowbotagents')
        cache['obs'] = mod.obs  # Return the _LazyObsModule instance, not the module
        return mod.obs
    if name == 'db':
        import importlib
        mod = importlib.import_module('.db', 'shadowbotagents')
        cache['db'] = mod
        return mod
    
    raise AttributeError(f"Not handled by custom_handler: {name}")


# Override the submodule with our function proxy
embedding = _global_embedding_proxy
embeddings = embedding  # embeddings is an alias


# Create the __getattr__ function using centralized utility
__getattr__ = create_lazy_getattr_with_fallback(
    mapping=_LAZY_IMPORTS,
    module_name=__name__,
    cache=_lazy_cache,
    fallback_modules=[],  # Note: 'embedding' excluded to avoid conflict with embedding() function
    custom_handler=_custom_handler
)


# Initialize telemetry only if explicitly enabled via config
def _init_telemetry():
    """Initialize telemetry if enabled via environment variable."""
    if not _config.TELEMETRY_ENABLED:
        return
    
    try:
        from .telemetry import get_telemetry
        from .telemetry.integration import auto_instrument_all
        
        _telemetry = get_telemetry()
        if _telemetry and _telemetry.enabled:
            use_performance_mode = _config.PERFORMANCE_MODE and not (
                _config.FULL_TELEMETRY or _config.AUTO_INSTRUMENT
            )
            auto_instrument_all(_telemetry, performance_mode=use_performance_mode)
            
            # Track package import for basic usage analytics
            try:
                _telemetry.track_feature_usage("package_import")
            except Exception:
                pass
    except Exception:
        # Silently fail if there are any issues - never break user applications
        pass


# Only initialize telemetry if explicitly enabled
_init_telemetry()


def warmup(include_litellm: bool = False, include_openai: bool = True) -> dict:
    """
    Pre-import heavy dependencies to reduce first-call latency.
    
    NOTE: For default OpenAI usage (llm="gpt-4o-mini"), warmup is NOT needed.
    The default path uses the native OpenAI SDK which is fast (~100ms import).
    
    Warmup is only beneficial when using LiteLLM backend, which is triggered by:
    - Using "/" in model name (e.g., llm="openai/gpt-4o-mini")
    - Passing a dict config (e.g., llm={"model": "gpt-4o-mini"})
    - Using base_url parameter
    
    Args:
        include_litellm: Pre-import LiteLLM (~2-3s). Only needed for multi-provider support.
        include_openai: Pre-import OpenAI SDK (~100ms). Default path, usually fast.
    
    Returns:
        dict: Timing information for each component warmed up
    
    Example:
        # For LiteLLM multi-provider usage:
        from shadowbotagents import warmup
        warmup(include_litellm=True)  # Pre-load LiteLLM
        
        agent = Agent(llm="anthropic/claude-3-sonnet")  # Now faster
        
        # For default OpenAI usage, no warmup needed:
        agent = Agent(llm="gpt-4o-mini")  # Already fast!
    """
    import time
    timings = {}
    
    if include_openai:
        start = time.perf_counter()
        try:
            import openai
            timings['openai'] = (time.perf_counter() - start) * 1000
        except ImportError:
            timings['openai'] = -1  # Not available
    
    if include_litellm:
        start = time.perf_counter()
        try:
            import litellm
            # Also configure litellm to avoid first-call overhead
            litellm.telemetry = False
            litellm.set_verbose = False
            litellm.drop_params = True
            litellm.modify_params = True
            timings['litellm'] = (time.perf_counter() - start) * 1000
        except ImportError:
            timings['litellm'] = -1  # Not available
    
    return timings


# ============================================================================
# PUBLIC API: __all__ (controls IDE autocomplete and `from X import *`)
# ============================================================================
# DESIGN: Keep __all__ minimal for clean IDE experience.
# All 186+ symbols are still accessible via __getattr__ for backwards compat.
# Organized imports available via sub-packages: config, tools, memory, workflows
# ============================================================================

__all__ = [
    # Core classes - the essentials
    'Agent',
    'AgentTeam',  # Primary class for multi-agent coordination (v1.0+)
    'AgentManager',  # Silent alias for AgentTeam
    'Agents',  # Deprecated alias for AgentTeam (emits warning)
    'Task',
    
    # AgentFlow (deterministic pipelines)
    'AgentFlow',  # Primary class for workflows (v1.0+)
    'Workflow',  # Silent alias for AgentFlow
    'Pipeline',  # Silent alias for AgentFlow
    
    # AgentOS (production deployment protocols)
    'AgentOSProtocol',  # Primary protocol for deployment (v1.0+)
    'AgentOSConfig',  # Primary config for deployment (v1.0+)
    'AgentAppProtocol',  # Silent alias for AgentOSProtocol
    'AgentAppConfig',  # Silent alias for AgentOSConfig
    
    # Tool essentials
    'tool',
    'Tools',
    
    # Approval (agent-centric approval backends)
    'AutoApproveBackend',
    
    # Embedding API - simplified imports
    # Usage: from shadowbotagents import embedding, EmbeddingResult
    'embedding',
    'embeddings',  # Plural alias (OpenAI style)
    'aembedding',
    'aembeddings',  # Plural alias for async
    'EmbeddingResult',
    'get_dimensions',
    
    # Autonomy
    'AutonomyConfig',
    'AutonomyLevel',
    
    # Sub-packages for organized imports
    # Usage: import shadowbotagents as pa; pa.config.MemoryConfig
    'config',
    'tools',
    'memory',
    'workflows',
]


def __dir__():
    """
    Return clean list for dir() - matches __all__ plus standard attributes.
    
    This keeps IDE autocomplete clean while preserving full backwards
    compatibility via __getattr__ for all 186+ legacy exports.
    """
    return list(__all__) + [
        # Standard module attributes
        '__name__', '__doc__', '__file__', '__path__', '__package__',
        '__loader__', '__spec__', '__cached__', '__builtins__',
    ]


# ============================================================================
# BACKWARDS COMPATIBILITY: Legacy __all__ items (for reference)
# ============================================================================
# All items below are still importable via __getattr__ but NOT in autocomplete:
# - ImageAgent, ContextAgent, create_context_agent, ShadowBotAgents
# - BaseTool, ToolResult, ToolValidationError, validate_tool, FunctionTool
# - ToolRegistry, get_registry, register_tool, get_tool
# - TaskOutput, ReflectionOutput, AutoAgents, AutoRagAgent, AutoRagConfig
# - Session, Memory, db, obs, Knowledge, Chunking
# - GuardrailResult, LLMGuardrail, Handoff, handoff, handoff_filters
# - MemoryConfig, KnowledgeConfig, PlanningConfig, OutputConfig, etc.
# - Workflow, Task, Route, Parallel, Loop, Repeat, Pipeline, etc.
# - MCP, FlowDisplay, track_workflow, FastContext, etc.
# - Plan, PlanStep, TodoList, PlanningAgent, ApprovalCallback, etc.
# - RAG, RAGConfig, RAGResult, AGUI, A2A, etc.
# - All telemetry, display, and utility functions
# ============================================================================
