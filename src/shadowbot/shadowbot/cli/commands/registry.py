"""
Registry command group for ShadowBot CLI.

Provides registry management commands.
"""

import typer

app = typer.Typer(help="Registry management")


@app.command("list")
def registry_list():
    """List registry entries."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['registry', 'list']
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("serve")
def registry_serve(
    port: int = typer.Option(8080, "--port", "-p", help="Port to serve on"),
):
    """Start registry server.
    
    DEPRECATED: Use `shadowbot serve registry` instead.
    """
    from shadowbot.cli.main import ShadowBot
    import sys
    
    # Print deprecation warning
    print("\n\033[93m⚠ DEPRECATION WARNING:\033[0m", file=sys.stderr)
    print("\033[93m'shadowbot registry serve' is deprecated and will be removed in a future version.\033[0m", file=sys.stderr)
    print("\033[93mPlease use 'shadowbot serve registry' instead.\033[0m\n", file=sys.stderr)
    
    argv = ['registry', 'serve', '--port', str(port)]
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
