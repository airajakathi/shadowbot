# ShadowBot Serve Examples

Examples for all ShadowBot server types and the unified endpoints CLI.

## Examples

| Example | Description | CLI Command |
|---------|-------------|-------------|
| `unified_server.py` | All providers in one server | `shadowbot serve unified` |
| `agent_as_api_single.py` | Single agent HTTP API | `shadowbot serve agents` |
| `agents_as_api_router.py` | Multi-agent router API | `shadowbot serve agents` |
| `a2a_server_client.py` | A2A protocol server | `shadowbot serve a2a` |
| `a2u_events_stream.py` | A2U event stream | `shadowbot serve a2u` |
| `mcp_http_server.py` | MCP HTTP server | `shadowbot serve mcp` |
| `tools_as_mcp_server.py` | Tools as MCP server | `shadowbot serve tools` |
| `agent_launch_modes.py` | Agent.launch() API | Python only |
| `endpoints_unified_client.py` | Unified client | `shadowbot endpoints` |
| `serve_example.py` | Recipe server client | `shadowbot recipe serve` |

## Server Commands

| Command | Description |
|---------|-------------|
| `shadowbot serve unified --port 8765` | Start unified server |
| `shadowbot serve agents --file agents.yaml --port 8000` | Start agents API |
| `shadowbot serve recipe --port 8765` | Start recipe server |
| `shadowbot serve mcp --transport http --port 8080` | Start MCP server |
| `shadowbot serve tools --port 8081` | Start tools MCP server |
| `shadowbot serve a2a --port 8082` | Start A2A server |
| `shadowbot serve a2u --port 8083` | Start A2U server |

## Client Commands

| Command | Description |
|---------|-------------|
| `shadowbot endpoints list` | List all endpoints |
| `shadowbot endpoints list --type agents-api` | Filter by type |
| `shadowbot endpoints describe <name>` | Get endpoint details |
| `shadowbot endpoints invoke <name> --input-json '{}'` | Invoke endpoint |
| `shadowbot endpoints health` | Check server health |
| `shadowbot endpoints types` | List provider types |
| `shadowbot endpoints discovery` | Show discovery document |

## Quick Start

```bash
# Terminal 1: Start unified server
export OPENAI_API_KEY=your-key
shadowbot serve unified --port 8765

# Terminal 2: Use endpoints CLI
shadowbot endpoints health
shadowbot endpoints list
shadowbot endpoints types
```

## Provider Types

| Type | Description |
|------|-------------|
| `recipe` | Recipe runner endpoints |
| `agents-api` | Single/multi-agent HTTP API |
| `mcp` | MCP server (stdio, http, sse) |
| `tools-mcp` | Tools exposed as MCP server |
| `a2a` | Agent-to-agent protocol |
| `a2u` | Agent-to-user event stream |

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `host` | Server bind address | 127.0.0.1 |
| `port` | Server port | 8765 |
| `auth` | Auth type (none, api-key, jwt) | none |
| `api_key` | API key for auth | - |
| `preload` | Preload recipes on startup | false |
| `recipes` | List of recipes to serve | all |
| `cors_origins` | CORS allowed origins | - |

## Advanced Features

| Feature | CLI Flag | Description | Docs |
|---------|----------|-------------|------|
| Rate Limiting | `--rate_limit 100` | Requests per minute per client | [Code](/docs/features/recipe-serve-advanced) [CLI](/docs/cli/recipe-serve-advanced) |
| Request Size Limit | `--max_request_size 10485760` | Max request body (bytes) | [Code](/docs/features/recipe-serve-advanced) [CLI](/docs/cli/recipe-serve-advanced) |
| Metrics Endpoint | `--enable_metrics` | Prometheus /metrics endpoint | [Code](/docs/features/recipe-serve-advanced) [CLI](/docs/cli/recipe-serve-advanced) |
| Admin Reload | `--enable_admin` | Hot reload /admin/reload | [Code](/docs/features/recipe-serve-advanced) [CLI](/docs/cli/recipe-serve-advanced) |
| Workers | `--workers 4` | Multi-process workers | [Code](/docs/features/recipe-serve-advanced) [CLI](/docs/cli/recipe-serve-advanced) |
| OpenTelemetry | `--trace_exporter otlp` | Distributed tracing | [Code](/docs/features/recipe-serve-advanced) [CLI](/docs/cli/recipe-serve-advanced) |
| OpenAPI | `GET /openapi.json` | API specification | [Code](/docs/features/recipe-serve-advanced) [CLI](/docs/cli/recipe-serve-advanced) |

## Advanced Examples

| Example | Description |
|---------|-------------|
| `recipe_serve_features.py` | All advanced features demo |

## Advanced CLI Commands

```bash
# Production server with all features
shadowbot recipe serve \
  --host 0.0.0.0 \
  --port 8765 \
  --auth api-key \
  --workers 4 \
  --rate_limit 100 \
  --enable_metrics \
  --enable_admin

# Get metrics
curl http://localhost:8765/metrics

# Get OpenAPI spec
curl http://localhost:8765/openapi.json

# Hot reload recipes
curl -X POST http://localhost:8765/admin/reload \
  -H "X-API-Key: your-key"
```

## CLI Commands

```bash
# Health check
shadowbot endpoints health

# List recipes (with auth)
shadowbot endpoints list --api-key your-key

# Invoke recipe
shadowbot endpoints invoke my-recipe \
  --input-json '{"query": "Hello"}' \
  --api-key your-key \
  --json
```

## Security Notes

- Always use `--auth api-key` when binding to `0.0.0.0`
- Store API keys in environment variables, not config files
- Use HTTPS in production (via reverse proxy)
