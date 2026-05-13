# Recipe Scheduler Example

This example demonstrates how to schedule recipes and agents to run periodically.

## Prerequisites

```bash
pip install shadowbot shadowbotagents
export OPENAI_API_KEY="your-api-key"
```

## Python Example

```bash
python example_scheduler.py
```

Press Ctrl+C to stop the scheduler and see statistics.

## CLI Examples

### Start a scheduler with task

```bash
# Basic scheduler
shadowbot schedule start news-checker "Check AI news" --interval hourly

# With timeout and budget
shadowbot schedule start reporter "Generate report" \
    --interval daily \
    --timeout 300 \
    --max-cost 1.00

# With max retries
shadowbot schedule start checker "Check updates" \
    --interval hourly \
    --max-retries 5
```

### Start a scheduler with recipe

```bash
# Schedule a recipe
shadowbot schedule start news-monitor --recipe news-analyzer --interval hourly

# With all options
shadowbot schedule start my-scheduler \
    --recipe my-recipe \
    --interval "*/6h" \
    --timeout 600 \
    --max-cost 2.00 \
    --max-retries 3
```

### Foreground mode (for testing)

```bash
# Run in foreground (Ctrl+C to stop)
shadowbot schedule "Check news" --interval "*/30s"
```

### Manage schedulers

```bash
# List all schedulers
shadowbot schedule list

# View logs
shadowbot schedule logs news-checker --follow

# Show statistics
shadowbot schedule stats news-checker

# Stop a scheduler
shadowbot schedule stop news-checker

# Stop all schedulers
shadowbot schedule stop-all

# Delete a scheduler
shadowbot schedule delete news-checker
```

### Export scheduler config

```bash
shadowbot schedule save news-checker --output news-checker.yaml
```

## Interval Formats

| Format | Description |
|--------|-------------|
| `hourly` | Every hour |
| `daily` | Every day |
| `*/30m` | Every 30 minutes |
| `*/6h` | Every 6 hours |
| `*/30s` | Every 30 seconds (for testing) |
| `3600` | Every 3600 seconds |

## Key Features

- **Periodic Execution**: Run tasks at regular intervals
- **Retry Logic**: Automatic retries on failure
- **Cost Budgeting**: Set spending limits
- **Daemon Mode**: Run in background
- **Statistics**: Track success rates

## Safe Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `interval` | hourly | Execution interval |
| `max_retries` | 3 | Retry attempts |
| `timeout` | 300 | Timeout per execution |
| `max_cost` | 1.00 | Budget limit (USD) |
