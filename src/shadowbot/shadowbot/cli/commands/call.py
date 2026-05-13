"""
Call command group for ShadowBot CLI.

Provides voice/call interaction commands.
"""

from typing import Optional

import typer

app = typer.Typer(help="Voice/call interaction mode")


@app.callback(invoke_without_command=True)
def call_main(
    ctx: typer.Context,
    model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model to use"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """
    Start voice/call interaction mode.
    
    Examples:
        shadowbot call
        shadowbot call --model gpt-4o
    """
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['call']
    if model:
        argv.extend(['--model', model])
    if verbose:
        argv.append('--verbose')
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
