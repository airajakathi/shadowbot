# Terminal-Bench 2.0 Integration with ShadowBot

This directory contains examples for integrating ShadowBot Agents with **Terminal-Bench 2.0** via the **Harbor framework** for AI agent benchmarking.

## Overview

[Terminal-Bench 2.0](https://tbench.ai) is a Stanford/Laude Institute benchmark that has become the gold standard for evaluating AI coding agents in real terminal environments. The [Harbor framework](https://harborframework.com) is the official evaluation harness that abstracts container lifecycle, parallelization, and cloud providers.

## Integration Types

### 1. External Agent (Direct Agent Class)
- **File**: `shadowbot_external_agent.py`
- **Purpose**: External agent that uses direct `Agent()` class instantiation
- **Usage**: Run with `--agent-import-path` flag
- **Approach**: Uses `shadowbotagents.Agent` directly with `execute_command` tool

### 2. Wrapper Agent (CLI-Based)
- **File**: `shadowbot_wrapper_agent.py`
- **Purpose**: Uses `shadowbot "TASK"` CLI pattern instead of direct Agent class
- **Usage**: Run with `--agent-import-path examples.terminal_bench.shadowbot_wrapper_agent:ShadowBotWrapperAgent`
- **Approach**: Installs `shadowbot` CLI inside container and runs tasks via subprocess
- **Best for**: Users who prefer CLI-style interface matching standard `shadowbot` usage

### 3. Installed Agent (Production)
- **File**: `shadowbot_installed_agent.py` 
- **Purpose**: Production-ready agent installed inside Harbor containers
- **Usage**: Integrates with Harbor's leaderboard system

## Quick Start

### Prerequisites

```bash
# Install Harbor framework
pip install harbor

# Install ShadowBot with shell tools
pip install shadowbotagents[tools]
```

### Running External Agent (Direct Agent Class)

```bash
# Test with oracle agent first
harbor run -d terminal-bench/terminal-bench-2 -a oracle

# Run ShadowBot external agent (uses direct Agent() class)
harbor run -d terminal-bench/terminal-bench-2 \
  --agent-import-path examples.terminal_bench.shadowbot_external_agent:ShadowBotExternalAgent \
  --model openai/gpt-4o \
  --ae OPENAI_API_KEY=$OPENAI_API_KEY \
  -n 4
```

### Running Wrapper Agent (CLI-Based)

```bash
# Run ShadowBot wrapper agent (uses `shadowbot "TASK"` CLI pattern)
harbor run -d terminal-bench/terminal-bench-2 \
  --agent-import-path examples.terminal_bench.shadowbot_wrapper_agent:ShadowBotWrapperAgent \
  --model openai/gpt-4o \
  --ae OPENAI_API_KEY=$OPENAI_API_KEY \
  -n 4
```

### Running on Cloud (Daytona/E2B/Modal)

```bash
harbor run -d terminal-bench/terminal-bench-2 \
  --agent-import-path examples.terminal_bench.shadowbot_external_agent:ShadowBotExternalAgent \
  --model openai/gpt-4o \
  --env daytona -n 32 \
  --ae OPENAI_API_KEY=$OPENAI_API_KEY
```

## Key Features

- **Shell Execution Bridge**: Wraps Harbor's `BaseEnvironment.exec()` as ShadowBot tool
- **Auto-Approval**: Bypasses `@require_approval` for container-isolated execution
- **Token Tracking**: Populates Harbor's `AgentContext` with usage metrics
- **API Key Forwarding**: Supports environment variable injection
- **Multi-Agent Support**: Can run `AgentTeam` and `AgentFlow` workflows

## Architecture

```text
┌─────────────────────────────────────────┐
│            Harbor Framework             │
│   (Terminal-Bench 2.0 Evaluation)      │
├─────────────────────────────────────────┤
│  BaseEnvironment.exec() ←→ bash_tool    │
├─────────────────────────────────────────┤
│         ShadowBot Agent                 │
│  • Uses execute_command tool            │
│  • Auto-approval for container safety  │
│  • Token tracking and metrics          │
└─────────────────────────────────────────┘
```

## Files

- `README.md` - This documentation
- `shadowbot_external_agent.py` - External agent (direct Agent class)
- `shadowbot_wrapper_agent.py` - Wrapper agent (CLI-based approach)
- `shadowbot_installed_agent.py` - Installed agent implementation  
- `multi_agent_example.py` - Multi-agent team example
- `job.yaml` - Example Harbor job configuration
- `test_basic.py` - Basic smoke tests
- `test_integration.py` - Integration tests
- `test_real_agentic.py` - Real agentic tests

## Terminal-Bench 2.0 Tasks

The benchmark includes 89 carefully curated tasks covering:
- Compiling code
- Training models  
- Setting up servers
- System administration
- File manipulation
- Package management

Each task provides:
- English instruction
- Docker container environment
- Test script (writes reward to `/logs/verifier/reward.txt`)
- Reference oracle solution

## Contributing

1. Test changes with oracle agent first: `harbor run -d terminal-bench/terminal-bench-2 -a oracle`
2. Run real agentic tests to ensure end-to-end functionality
3. Follow ShadowBot's AGENTS.md architecture guidelines
4. Add both unit tests and integration tests

## Resources

- [Terminal-Bench 2.0 Announcement](https://www.tbench.ai/news/announcement-2-0)
- [Harbor Framework Docs](https://www.harborframework.com/docs)
- [Terminal-Bench Leaderboard](https://tbench.ai/leaderboard)
- [Harbor GitHub Repo](https://github.com/laude-institute/harbor)