"""
Todo command group for ShadowBot CLI.

Provides todo/task management commands.
"""

import typer

app = typer.Typer(help="Todo/task management")


@app.command("list")
def todo_list():
    """List todos."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['todo', 'list']
    
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
def todo_add(
    task: str = typer.Argument(..., help="Task description"),
    priority: str = typer.Option("medium", "--priority", "-p", help="Priority (low, medium, high)"),
):
    """Add a todo."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['todo', 'add', task]
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv


@app.command("done")
def todo_done(
    task_id: str = typer.Argument(..., help="Task ID to mark as done"),
):
    """Mark a todo as done."""
    from shadowbot.cli.main import ShadowBot
    import sys
    
    argv = ['todo', 'done', task_id]
    
    original_argv = sys.argv
    sys.argv = ['shadowbot'] + argv
    
    try:
        praison = ShadowBot()
        praison.main()
    except SystemExit:
        pass
    finally:
        sys.argv = original_argv
