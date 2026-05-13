# Recipe Async Jobs Example

This example demonstrates how to submit recipes as async jobs to a jobs server.

## Prerequisites

```bash
pip install shadowbot shadowbotagents httpx uvicorn
export OPENAI_API_KEY="your-api-key"
```

## Start the Jobs Server

```bash
python -m uvicorn shadowbot.jobs.server:create_app --port 8005 --factory
```

## Python Example

```bash
python example_jobs.py
```

## CLI Examples

### Submit a job

```bash
# Basic submission
shadowbot run submit "Analyze AI trends"

# Submit with recipe
shadowbot run submit "Analyze news" --recipe news-analyzer

# Wait for completion
shadowbot run submit "Quick task" --wait

# Stream progress
shadowbot run submit "Long task" --stream

# With webhook
shadowbot run submit "Task" --webhook-url https://example.com/callback

# With idempotency
shadowbot run submit "Task" --idempotency-key order-123

# With metadata
shadowbot run submit "Task" --metadata user=john --metadata priority=high
```

### Check status

```bash
shadowbot run status <job_id>
shadowbot run status <job_id> --json
```

### Get result

```bash
shadowbot run result <job_id>
shadowbot run result <job_id> --json
```

### Stream progress

```bash
shadowbot run stream <job_id>
```

### List jobs

```bash
shadowbot run list
shadowbot run list --status running
```

### Cancel job

```bash
shadowbot run cancel <job_id>
```

## Key Features

- **Server-based**: Jobs persist across restarts
- **Webhooks**: Get notified when jobs complete
- **Idempotency**: Prevent duplicate submissions
- **Streaming**: Real-time progress updates
- **Metadata**: Attach custom data to jobs

## Safe Defaults

| Setting | Default | Description |
|---------|---------|-------------|
| `timeout` | 3600 | Maximum execution time (1 hour) |
| `api_url` | http://127.0.0.1:8005 | Jobs server URL |
