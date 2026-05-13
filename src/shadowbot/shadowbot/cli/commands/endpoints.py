"""
Endpoints command group for ShadowBot CLI.

Provides API endpoint management commands.
"""

import typer

app = typer.Typer(help="API endpoint management")


@app.command("list")
def endpoints_list():
    """List available endpoints."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['endpoints', 'list']
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("test")
def endpoints_test(
    endpoint: str = typer.Argument(..., help="Endpoint to test"),
):
    """Test an endpoint."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['endpoints', 'test', endpoint]
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
