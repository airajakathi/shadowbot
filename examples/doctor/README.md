# ShadowBot Doctor Examples

Examples demonstrating the ShadowBot Doctor health check and diagnostics system.

## CLI Examples

| Command | Description |
|---------|-------------|
| `shadowbot doctor` | Run all fast health checks |
| `shadowbot doctor --version` | Show doctor version |
| `shadowbot doctor --list-checks` | List all available checks |
| `shadowbot doctor env` | Check environment configuration |
| `shadowbot doctor config` | Validate configuration files |
| `shadowbot doctor tools` | Check tool availability |
| `shadowbot doctor db` | Check database drivers |
| `shadowbot doctor mcp` | Check MCP configuration |
| `shadowbot doctor obs` | Check observability providers |
| `shadowbot doctor skills` | Check agent skills |
| `shadowbot doctor memory` | Check memory storage |
| `shadowbot doctor permissions` | Check filesystem permissions |
| `shadowbot doctor network` | Check network connectivity |
| `shadowbot doctor performance` | Check import times |
| `shadowbot doctor ci` | CI mode with JSON output |
| `shadowbot doctor selftest` | Test agent functionality |

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output in JSON format |
| `--format text\|json` | Output format |
| `--output PATH` | Write report to file |
| `--deep` | Enable deeper probes |
| `--timeout SEC` | Per-check timeout |
| `--strict` | Treat warnings as failures |
| `--quiet` | Minimal output |
| `--no-color` | Disable colors |
| `--only IDS` | Only run these checks |
| `--skip IDS` | Skip these checks |

## Python Examples

| File | Description |
|------|-------------|
| [basic_doctor.py](basic_doctor.py) | Programmatic health checks |
| [ci_integration.py](ci_integration.py) | CI/CD pipeline integration |

## Quick Start

```bash
# Run basic health checks
shadowbot doctor

# Run with JSON output
shadowbot doctor --json

# Run specific checks
shadowbot doctor --only python_version,openai_api_key

# CI mode
shadowbot doctor ci

# Save report to file
shadowbot doctor --output report.json
```
