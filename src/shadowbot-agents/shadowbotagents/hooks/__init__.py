"""
Hooks Module for ShadowBot Agents.

Provides a powerful hook system for intercepting and modifying agent behavior
at various lifecycle points. Unlike callbacks (which are for UI events),
hooks can intercept, modify, or block tool execution.

Features:
- Event-based hook system (BeforeTool, AfterTool, BeforeAgent, etc.)
- Shell command hooks for external integrations
- Python function hooks for in-process customization
- Matcher patterns for selective hook execution
- Sequential and parallel hook execution
- Decision outcomes (allow, deny, block, ask)

Zero Performance Impact:
- All imports are lazy loaded via centralized _lazy.py utility
- Hooks only execute when registered
- No overhead when hooks are disabled

Usage:
    from shadowbotagents.hooks import HookRegistry, HookEvent
    
    # Register a Python function hook
    registry = HookRegistry()
    
    @registry.on(HookEvent.BEFORE_TOOL)
    def my_hook(event_data):
        if event_data.tool_name == "dangerous_tool":
            return HookResult(decision="deny", reason="Tool blocked by policy")
        return HookResult(decision="allow")
    
    # Register a shell command hook
    registry.register_command_hook(
        event=HookEvent.BEFORE_TOOL,
        command="python /path/to/validator.py",
        matcher="write_*"  # Only match tools starting with write_
    )
    
    # Use with Agent
    agent = Agent(
        name="MyAgent",
        hooks=registry
    )
"""

from .._lazy import create_lazy_getattr_with_groups

__all__ = [
    # Core types
    "HookEvent",
    "HookDecision",
    "HookResult",
    "HookInput",
    "HookOutput",
    # Hook definitions
    "HookDefinition",
    "CommandHook",
    "FunctionHook",
    # Registry and runner
    "HookRegistry",
    "HookRunner",
    # Event-specific inputs
    "BeforeToolInput",
    "AfterToolInput",
    "BeforeAgentInput",
    "AfterAgentInput",
    "BeforeLLMInput",
    "AfterLLMInput",
    "SessionStartInput",
    "SessionEndInput",
    "OnErrorInput",
    "OnRetryInput",
    # Message lifecycle event inputs
    "MessageReceivedInput",
    "MessageSendingInput",
    "MessageSentInput",
    # Middleware types
    "InvocationContext",
    "ModelRequest",
    "ModelResponse",
    "ToolRequest",
    "ToolResponse",
    # Middleware decorators
    "before_model",
    "after_model",
    "wrap_model_call",
    "before_tool",
    "after_tool",
    "wrap_tool_call",
    # Middleware utilities
    "MiddlewareChain",
    "AsyncMiddlewareChain",
    "MiddlewareManager",
    # Verification hooks (protocols)
    "VerificationHook",
    "VerificationResult",
    # Simplified API (beginner-friendly)
    "add_hook",
    "remove_hook",
    "has_hook",
    "get_default_registry",
]

# Grouped lazy imports for DRY and efficient loading
# When one attribute from a group is accessed, all are loaded together
_LAZY_GROUPS = {
    'types_core': {
        'HookEvent': ('shadowbotagents.hooks.types', 'HookEvent'),
        'HookDecision': ('shadowbotagents.hooks.types', 'HookDecision'),
        'HookResult': ('shadowbotagents.hooks.types', 'HookResult'),
        'HookInput': ('shadowbotagents.hooks.types', 'HookInput'),
        'HookOutput': ('shadowbotagents.hooks.types', 'HookOutput'),
    },
    'types_definitions': {
        'HookDefinition': ('shadowbotagents.hooks.types', 'HookDefinition'),
        'CommandHook': ('shadowbotagents.hooks.types', 'CommandHook'),
        'FunctionHook': ('shadowbotagents.hooks.types', 'FunctionHook'),
    },
    'registry': {
        'HookRegistry': ('shadowbotagents.hooks.registry', 'HookRegistry'),
    },
    'runner': {
        'HookRunner': ('shadowbotagents.hooks.runner', 'HookRunner'),
    },
    'events': {
        'BeforeToolInput': ('shadowbotagents.hooks.events', 'BeforeToolInput'),
        'AfterToolInput': ('shadowbotagents.hooks.events', 'AfterToolInput'),
        'BeforeAgentInput': ('shadowbotagents.hooks.events', 'BeforeAgentInput'),
        'AfterAgentInput': ('shadowbotagents.hooks.events', 'AfterAgentInput'),
        'BeforeLLMInput': ('shadowbotagents.hooks.events', 'BeforeLLMInput'),
        'AfterLLMInput': ('shadowbotagents.hooks.events', 'AfterLLMInput'),
        'SessionStartInput': ('shadowbotagents.hooks.events', 'SessionStartInput'),
        'SessionEndInput': ('shadowbotagents.hooks.events', 'SessionEndInput'),
        'OnErrorInput': ('shadowbotagents.hooks.events', 'OnErrorInput'),
        'OnRetryInput': ('shadowbotagents.hooks.events', 'OnRetryInput'),
        'MessageReceivedInput': ('shadowbotagents.hooks.events', 'MessageReceivedInput'),
        'MessageSendingInput': ('shadowbotagents.hooks.events', 'MessageSendingInput'),
        'MessageSentInput': ('shadowbotagents.hooks.events', 'MessageSentInput'),
    },
    'middleware_types': {
        'InvocationContext': ('shadowbotagents.hooks.middleware', 'InvocationContext'),
        'ModelRequest': ('shadowbotagents.hooks.middleware', 'ModelRequest'),
        'ModelResponse': ('shadowbotagents.hooks.middleware', 'ModelResponse'),
        'ToolRequest': ('shadowbotagents.hooks.middleware', 'ToolRequest'),
        'ToolResponse': ('shadowbotagents.hooks.middleware', 'ToolResponse'),
    },
    'middleware_decorators': {
        'before_model': ('shadowbotagents.hooks.middleware', 'before_model'),
        'after_model': ('shadowbotagents.hooks.middleware', 'after_model'),
        'wrap_model_call': ('shadowbotagents.hooks.middleware', 'wrap_model_call'),
        'before_tool': ('shadowbotagents.hooks.middleware', 'before_tool'),
        'after_tool': ('shadowbotagents.hooks.middleware', 'after_tool'),
        'wrap_tool_call': ('shadowbotagents.hooks.middleware', 'wrap_tool_call'),
    },
    'middleware_utilities': {
        'MiddlewareChain': ('shadowbotagents.hooks.middleware', 'MiddlewareChain'),
        'AsyncMiddlewareChain': ('shadowbotagents.hooks.middleware', 'AsyncMiddlewareChain'),
        'MiddlewareManager': ('shadowbotagents.hooks.middleware', 'MiddlewareManager'),
    },
    'verification': {
        'VerificationHook': ('shadowbotagents.hooks.verification', 'VerificationHook'),
        'VerificationResult': ('shadowbotagents.hooks.verification', 'VerificationResult'),
    },
    # Simplified API (beginner-friendly aliases)
    'simplified_api': {
        'add_hook': ('shadowbotagents.hooks.registry', 'add_hook'),
        'remove_hook': ('shadowbotagents.hooks.registry', 'remove_hook'),
        'has_hook': ('shadowbotagents.hooks.registry', 'has_hook'),
        'get_default_registry': ('shadowbotagents.hooks.registry', 'get_default_registry'),
    },
}

# Create the __getattr__ function using centralized utility
__getattr__ = create_lazy_getattr_with_groups(_LAZY_GROUPS, __name__)
