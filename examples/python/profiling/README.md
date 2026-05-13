# ShadowBot Profiling Examples

This directory contains examples for profiling ShadowBot agent performance.

## Prerequisites

```bash
pip install shadowbot
export OPENAI_API_KEY=your_key_here
```

## Examples

### 1. Basic Profiling (`basic_profiling.py`)

Demonstrates programmatic profiling of a single query:

```bash
python basic_profiling.py
```

### 2. Suite Profiling (`suite_profiling.py`)

Runs a comprehensive profiling suite with multiple scenarios:

```bash
python suite_profiling.py
```

### 3. Optimization Demo (`optimization_example.py`)

Demonstrates Tier 0/1/2 performance optimizations:

```bash
python optimization_example.py
```

## CLI Commands

You can also profile directly from the command line:

```bash
# Profile a query
shadowbot profile query "What is 2+2?"

# Profile with file grouping
shadowbot profile query "Hello" --show-files --limit 20

# Profile imports
shadowbot profile imports

# Profile startup time
shadowbot profile startup

# Run comprehensive suite
shadowbot profile suite --quick

# Create performance baseline
shadowbot profile snapshot --baseline

# Compare against baseline
shadowbot profile snapshot current --compare

# Show optimization status
shadowbot profile optimize --show
```

## Output

- **Text output**: Human-readable timing breakdown
- **JSON output**: Machine-readable for CI/CD (`--format json`)
- **Artifacts**: Binary cProfile data and reports (`--save ./results`)
- **Snapshots**: Performance baselines for regression detection

## Performance Optimizations

Enable opt-in optimizations via environment variables:

```bash
export PRAISONAI_LITE_MODE=1
export PRAISONAI_SKIP_TYPE_VALIDATION=1
export PRAISONAI_MINIMAL_IMPORTS=1
```
