"""
ShadowBot Langextract Commands.

CLI commands for rendering ShadowBot traces with langextract:
- `shadowbot langextract view` - render existing JSONL to HTML
- `shadowbot langextract render` - run workflow with langextract observability
"""

import typer
import webbrowser
from pathlib import Path
from typing import Optional

app = typer.Typer(name="langextract", help="Render ShadowBot traces with langextract.")


@app.command(name="view")
def view(
    jsonl_path: Path = typer.Argument(..., help="Path to annotated-documents JSONL"),
    output_html: Path = typer.Option("trace.html", "--output", "-o", help="Output HTML file path"),
    no_open: bool = typer.Option(False, "--no-open", help="Don't open HTML in browser"),
):
    """Render an existing annotated-documents JSONL to an interactive HTML."""
    try:
        import langextract as lx  # type: ignore
    except ImportError:
        typer.echo("Error: langextract is not installed. Install with: pip install 'shadowbot[langextract]'", err=True)
        raise typer.Exit(1)

    if not jsonl_path.exists():
        typer.echo(f"Error: JSONL file not found: {jsonl_path}", err=True)
        raise typer.Exit(1)

    try:
        html = lx.visualize(str(jsonl_path))
        html_text = html.data if hasattr(html, "data") else html
        output_html.write_text(html_text, encoding="utf-8")
        typer.echo(f"✅ Wrote {output_html}")
        
        if not no_open:
            webbrowser.open(f"file://{output_html.resolve()}")
    except Exception as e:
        typer.echo(f"Error: Failed to render HTML: {e}", err=True)
        raise typer.Exit(1)


@app.command(name="render")
def render(
    yaml_path: Path = typer.Argument(..., help="ShadowBot YAML workflow"),
    output_html: Path = typer.Option("workflow.html", "--output", "-o", help="Output HTML file path"),
    no_open: bool = typer.Option(False, "--no-open", help="Don't open HTML in browser"),
    api_url: Optional[str] = typer.Option(None, "--api-url", help="API URL (if using remote API)"),
):
    """Run a workflow end-to-end with LangextractSink attached, then open the HTML."""
    try:
        import langextract  # noqa: F401 — probe optional dep early for clear error
        from shadowbot.observability import LangextractSink, LangextractSinkConfig
        from shadowbotagents.trace.protocol import TraceEmitter, set_default_emitter
        from shadowbot import ShadowBot
    except ImportError as e:
        typer.echo(
            f"Error: Missing dependencies: {e}. "
            "Install langextract with: pip install 'shadowbot[langextract]'",
            err=True,
        )
        raise typer.Exit(1) from e

    if not yaml_path.exists():
        typer.echo(f"Error: YAML file not found: {yaml_path}", err=True)
        raise typer.Exit(1)

    # Set up langextract observability
    config = LangextractSinkConfig(
        output_path=str(output_html),
        auto_open=not no_open,
    )
    sink = LangextractSink(config=config)
    
    # Set up trace emitter for the duration of the run
    emitter = TraceEmitter(sink=sink, enabled=True)
    set_default_emitter(emitter)

    # Also bridge the context emitter so real agent runtime events
    # (agent_start/end, tool_call_*, llm_response) are captured.
    from shadowbot.observability.langextract import LangextractSink
    
    def warn_handler(msg: str):
        # Warn user about bridge failure since this command specifically generates traces
        typer.echo(f"Warning: {msg}", err=True)
        
    LangextractSink.bridge_context_events(
        sink=sink,
        session_id="shadowbot-langextract-render",
        warn_callback=warn_handler
    )
    
    try:
        # Run the workflow
        praison = ShadowBot(agent_file=str(yaml_path))
        if api_url:
            praison.api_url = api_url.rstrip("/")
        
        result = praison.main()
        typer.echo(result)
        
    except Exception as e:
        typer.echo(f"Error: Workflow failed: {e}", err=True)
        raise typer.Exit(1) from e
    finally:
        # Ensure sink is closed even if workflow fails
        sink.close()

    if output_html.exists():
        typer.echo(f"✅ Trace rendered: {output_html}")
    else:
        typer.echo(
            f"Error: Trace was not rendered to {output_html} (see logs for details)",
            err=True,
        )
        raise typer.Exit(1)