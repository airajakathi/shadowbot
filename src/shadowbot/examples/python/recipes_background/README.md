# Recipe Background Tasks Example

This example demonstrates how to run recipes and agents as background tasks.

## Prerequisites

```bash
pip install shadowbot shadowbotagents
export OPENAI_API_KEY="your-api-key"
```

## Python Example

```bash
python example_background.py
```

## CLI Examples

### Submit a recipe as background task

```bash
# Submit recipe to background
shadowbot background submit --recipe my-recipe --input '{"query": "test"}'

# Check status
shadowbot background status <task_id>

# List all tasks
shadowbot background list

# Cancel a task
shadowbot background cancel <task_id>

# Clear completed tasks
shadowbot background clear
```

### Run recipe with --background flag

```bash
# Run recipe in background
shadowbot recipe run my-recipe --background

# With input
shadowbot recipe run my-recipe --background --input '{"topic": "AI"}'

# With session ID
shadowbot recipe run my-recipe --background --session-id session_123
```

## Key Features

- **Async Execution**: Tasks run in the background without blocking
- **Progress Tracking**: Monitor task progress and status
- **Cancellation**: Cancel running tasks when needed
- **Result Retrieval**: Get results when tasks complete
- **Concurrency Control**: Limit concurrent tasks

## Safe Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `timeout_sec` | 300 | Maximum execution time |
| `max_concurrent` | 5 | Maximum concurrent tasks |
| `cleanup_delay_sec` | 3600 | Auto-cleanup delay |
