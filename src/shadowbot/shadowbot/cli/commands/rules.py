"""
Rules command group for ShadowBot CLI.

Provides rules management commands.
"""

import typer

app = typer.Typer(help="Rules management")


@app.command("list")
def rules_list():
    """List active rules."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['rules', 'list']
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("add")
def rules_add(
    rule: str = typer.Argument(..., help="Rule to add"),
):
    """Add a rule."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['rules', 'add', rule]
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("clear")
def rules_clear():
    """Clear all rules."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['rules', 'clear']
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
