"""
ShadowBot CLI Package

This package provides the command-line interface for ShadowBot.

Structure:
- ../.__main__.py: Unified CLI entry point (Typer-first, legacy fallback)
- app.py: Typer app with all command registrations
- main.py: Legacy argparse ShadowBot class (used for prompts/YAML)
- commands/: Individual Typer command modules
- features/: Feature handlers for CLI flags and commands
"""

__all__ = ["ShadowBot"]


def __getattr__(name):
    """Lazy load ShadowBot to avoid slow imports."""
    if name == "ShadowBot":
        from .main import ShadowBot
        return ShadowBot
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def main():
    """CLI entry point function."""
    from shadowbot.__main__ import main as _main
    _main()
