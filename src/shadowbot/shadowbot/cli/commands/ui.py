"""
UI command — launch the ShadowBot Clean Chat UI.

Usage:
    shadowbot ui                    # Chat on :8081
    shadowbot ui --port 9000        # Custom port
    shadowbot ui --app my-chat.py   # Custom app file
"""

import sys
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(help="🤖 ShadowBot Clean Chat UI")

UI_DIR = Path.home() / ".shadowbot" / "ui"
DEFAULT_APP = UI_DIR / "app.py"


def _ensure_default_app() -> Path:
    """Copy bundled default_app.py to ~/.shadowbot/ui/app.py if missing."""
    if DEFAULT_APP.exists():
        return DEFAULT_APP

    UI_DIR.mkdir(parents=True, exist_ok=True)

    # Read the bundled default
    bundled = Path(__file__).parent.parent.parent / "ui_chat" / "default_app.py"
    if not bundled.exists():
        print(f"\033[91mERROR: Bundled default_app.py not found at {bundled}\033[0m")
        raise typer.Abort()

    DEFAULT_APP.write_text(bundled.read_text())
    print(f"   ✓ Created default chat config: {DEFAULT_APP}")
    return DEFAULT_APP


def _launch_aiui_app(
    app_dir: str,
    default_app_name: str,
    port: int,
    host: str,
    app_file: Optional[str],
    reload: bool,
    ui_name: str
) -> None:
    """Common function to launch aiui apps."""
    # 1. Check shadowbotui is installed
    try:
        import importlib.util
        if importlib.util.find_spec("shadowbotui") is None:
            raise ImportError
    except ImportError:
        print(f"\n\033[91mERROR: ShadowBot UI (aiui) is not installed.\033[0m")
        print('\nInstall with:\n  pip install "shadowbot[ui]"\n')
        sys.exit(1)

    # 2. Resolve app file
    if app_file:
        resolved = Path(app_file)
        if not resolved.exists():
            print(f"\033[91mERROR: App file not found: {app_file}\033[0m")
            sys.exit(1)
    else:
        ui_dir = Path.home() / ".shadowbot" / app_dir
        default_app = ui_dir / "app.py"
        
        # Ensure default app exists
        if not default_app.exists():
            ui_dir.mkdir(parents=True, exist_ok=True)
            bundled = Path(__file__).parent.parent.parent / default_app_name / "default_app.py"
            if not bundled.exists():
                print(f"\033[91mERROR: Bundled default_app.py not found at {bundled}\033[0m")
                sys.exit(1)
            default_app.write_text(bundled.read_text())
            print(f"   ✓ Created default {ui_name} config: {default_app}")
        
        resolved = default_app

    # 3. Launch via aiui run
    import subprocess

    cmd = ["aiui", "run", str(resolved), "--port", str(port), "--host", host]
    if reload:
        cmd.append("--reload")

    print(f"\n🤖 ShadowBot {ui_name} starting at http://{host}:{port}")
    print(f"   App: {resolved}\n")

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
        print(f"\n🤖 {ui_name} stopped.")


@app.callback(invoke_without_command=True)
def ui(
    ctx: typer.Context,
    port: int = typer.Option(8081, "--port", "-p", help="Port to run chat UI on"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host to bind to"),
    app_file: Optional[str] = typer.Option(
        None, "--app", "-a", help="Custom app.py file (default: ~/.shadowbot/ui/app.py)"
    ),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
):
    """
    Launch the ShadowBot Clean Chat UI.

    Starts a clean chat interface powered by ShadowBotUI — no sidebar,
    single-page chat experience.

    For the full dashboard with agents, memory, knowledge, etc.,
    use: shadowbot claw

    Examples:
        shadowbot ui
        shadowbot ui --port 9000
        shadowbot ui --app my-chat.py
        shadowbot ui agents    # YAML agents dashboard
        shadowbot ui bot       # Bot interface
        shadowbot ui realtime  # Voice realtime
    """
    if ctx.invoked_subcommand is not None:
        return

    # Use legacy implementation for backward compatibility
    # 1. Check shadowbotui is installed
    try:
        import importlib.util
        if importlib.util.find_spec("shadowbotui") is None:
            raise ImportError
    except ImportError:
        print("\n\033[91mERROR: ShadowBot UI (aiui) is not installed.\033[0m")
        print('\nInstall with:\n  pip install "shadowbot[ui]"\n')
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

    print(f"\n🤖 ShadowBot Chat starting at http://{host}:{port}")
    print(f"   App: {resolved}\n")

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
        print("\n🤖 Chat stopped.")


@app.command()
def agents(
    port: int = typer.Option(8083, "--port", "-p", help="Port to run agents UI on"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host to bind to"),
    app_file: Optional[str] = typer.Option(
        None, "--app", "-a", help="Custom app.py file"
    ),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
):
    """
    Launch YAML Agents Dashboard.
    
    Replaces the old Chainlit agents interface with aiui.
    Loads agents from agents.yaml in the current directory.
    """
    _launch_aiui_app("ui_agents", "ui_agents", port, host, app_file, reload, "Agents Dashboard")


@app.command()
def bot(
    port: int = typer.Option(8084, "--port", "-p", help="Port to run bot UI on"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host to bind to"),
    app_file: Optional[str] = typer.Option(
        None, "--app", "-a", help="Custom app.py file"
    ),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
):
    """
    Launch Bot Interface.
    
    Replaces the old Chainlit bot interface with aiui.
    Provides step-by-step interaction visualization.
    """
    _launch_aiui_app("ui_bot", "ui_bot", port, host, app_file, reload, "Bot Interface")


@app.command()
def realtime(
    port: int = typer.Option(8085, "--port", "-p", help="Port to run realtime UI on"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host to bind to"),
    app_file: Optional[str] = typer.Option(
        None, "--app", "-a", help="Custom app.py file"
    ),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
):
    """
    Launch Realtime Voice Interface.
    
    Uses aiui's OpenAIRealtimeManager for WebRTC voice conversations.
    """
    _launch_aiui_app("ui_realtime", "ui_realtime", port, host, app_file, reload, "Realtime Voice")
