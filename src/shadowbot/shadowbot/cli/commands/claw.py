"""
Claw command — launch the ShadowBot 🦞 Dashboard.

Usage:
    shadowbot claw                # Dashboard on :8082
    shadowbot claw --port 9000    # Custom port
    shadowbot claw --app my.py    # Custom app file
"""

import sys
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(help="🦞 ShadowBot Dashboard (full UI)")

CLAW_DIR = Path.home() / ".shadowbot" / "claw"
DEFAULT_APP = CLAW_DIR / "app.py"


def _ensure_default_app() -> Path:
    """Copy bundled default_app.py to ~/.shadowbot/claw/app.py if missing."""
    if DEFAULT_APP.exists():
        return DEFAULT_APP

    CLAW_DIR.mkdir(parents=True, exist_ok=True)

    # Read the bundled default
    bundled = Path(__file__).parent.parent.parent / "claw" / "default_app.py"
    if not bundled.exists():
        print(f"[red]ERROR: Bundled default_app.py not found at {bundled}[/red]")
        raise typer.Abort()

    DEFAULT_APP.write_text(bundled.read_text())
    print(f"   ✓ Created default dashboard config: {DEFAULT_APP}")
    return DEFAULT_APP


@app.callback(invoke_without_command=True)
def claw(
    ctx: typer.Context,
    port: int = typer.Option(8082, "--port", "-p", help="Port to run dashboard on"),
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        help=(
            "Host to bind to (default: 127.0.0.1 — loopback only). "
            "Pass 0.0.0.0 to expose on the LAN; see docs for auth setup."
        ),
    ),
    app_file: Optional[str] = typer.Option(
        None, "--app", "-a", help="Custom app.py file (default: ~/.shadowbot/claw/app.py)"
    ),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
):
    """
    Launch the ShadowBot 🦞 Dashboard.

    Starts the AIUI dashboard with chat, agents, memory, knowledge,
    channels, cron, guardrails, and more.

    Examples:
        shadowbot claw
        shadowbot claw --port 9000
        shadowbot claw --app my-dashboard.py
    """
    if ctx.invoked_subcommand is not None:
        return

    # 1. Check shadowbotui is installed
    try:
        import importlib.util
        if importlib.util.find_spec("shadowbotui") is None:
            raise ImportError
    except ImportError:
        print("\n\033[91mERROR: ShadowBot Dashboard (aiui) is not installed.\033[0m")
        print('\nInstall with:\n  pip install "shadowbot[claw]"\n')
        sys.exit(1)

    # 2. Resolve app file
    if app_file:
        resolved = Path(app_file)
        if not resolved.exists():
            print(f"\033[91mERROR: App file not found: {app_file}\033[0m")
            sys.exit(1)
    else:
        resolved = _ensure_default_app()

    # 3. Launch via aiui run
    import subprocess

    cmd = ["aiui", "run", str(resolved), "--port", str(port), "--host", host]
    if reload:
        cmd.append("--reload")

    print(f"\n🦞 ShadowBot Dashboard starting at http://{host}:{port}")
    print(f"   App: {resolved}")
    # Warn if the user has opted into LAN exposure. The dashboard has no
    # built-in auth at the URL layer (see AuthConfig in shadowbotui), so
    # binding to a non-loopback address without extra guarding is risky.
    if host not in ("127.0.0.1", "localhost", "::1"):
        print(
            "\n\033[93m⚠  WARNING:\033[0m "
            f"Dashboard is bound to {host} — reachable from other hosts on your network.\n"
            "   The dashboard has no URL-level auth. For multi-user / remote use,\n"
            "   put it behind a reverse proxy or set shadowbotui AUTH_ENFORCE=true."
        )
    print("")

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        # Fallback: python -m shadowbotui.cli
        cmd = [sys.executable, "-m", "shadowbotui.cli", "run", str(resolved),
               "--port", str(port), "--host", host]
        if reload:
            cmd.append("--reload")
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🦞 Dashboard stopped.")
