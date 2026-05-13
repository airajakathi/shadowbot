"""
Doctor CLI module for ShadowBot.

Provides comprehensive health checks, diagnostics, and validation for the ShadowBot ecosystem.

Commands:
    shadowbot doctor              - Run fast default checks
    shadowbot doctor env          - Environment and API key validation
    shadowbot doctor config       - Configuration file validation
    shadowbot doctor tools        - Tool availability checks
    shadowbot doctor db           - Database connectivity checks
    shadowbot doctor mcp          - MCP server validation
    shadowbot doctor obs          - Observability provider checks
    shadowbot doctor skills       - Agent skills validation
    shadowbot doctor memory       - Memory/session storage checks
    shadowbot doctor permissions  - Filesystem permission checks
    shadowbot doctor network      - Network connectivity checks
    shadowbot doctor performance  - Import time analysis
    shadowbot doctor ci           - CI-optimized checks
    shadowbot doctor selftest     - Minimal agent dry-run
"""

__version__ = "1.0.0"

__all__ = [
    "DoctorHandler",
    "DoctorEngine",
    "CheckResult",
    "CheckStatus",
    "DoctorReport",
    "CheckRegistry",
    "TextFormatter",
    "JsonFormatter",
]


def __getattr__(name: str):
    """Lazy load doctor components to minimize import overhead."""
    if name == "DoctorHandler":
        from .handler import DoctorHandler
        return DoctorHandler
    elif name == "DoctorEngine":
        from .engine import DoctorEngine
        return DoctorEngine
    elif name == "CheckResult":
        from .models import CheckResult
        return CheckResult
    elif name == "CheckStatus":
        from .models import CheckStatus
        return CheckStatus
    elif name == "DoctorReport":
        from .models import DoctorReport
        return DoctorReport
    elif name == "CheckRegistry":
        from .registry import CheckRegistry
        return CheckRegistry
    elif name == "TextFormatter":
        from .formatters import TextFormatter
        return TextFormatter
    elif name == "JsonFormatter":
        from .formatters import JsonFormatter
        return JsonFormatter
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
