#!/usr/bin/env python3
"""
Comprehensive Quick Benchmark - ShadowBot vs Agno

All-in-one benchmark comparing two frameworks across multiple metrics:
- Import time (cold start)
- Agent instantiation time
- Memory footprint (per-agent)
- Function call count (cProfile)
- Deep profiling (hot spots)

Designed for rapid iteration with minimal iterations.

Usage:
    python benchmarks/quick_benchmark.py              # All metrics
    python benchmarks/quick_benchmark.py --fast       # Quick mode (fewer iterations)
    python benchmarks/quick_benchmark.py --profile    # Include cProfile details
    python benchmarks/quick_benchmark.py --memory     # Include memory details
    python benchmarks/quick_benchmark.py --import     # Include import time
    python benchmarks/quick_benchmark.py --all        # All detailed output
"""

import time
import argparse
import sys
import gc

# ============================================================================
# BENCHMARK FUNCTIONS
# ============================================================================

def measure_import_time(module_name, clear_cache=True, full_agent_import=True):
    """Measure import time for a module.
    
    Args:
        module_name: Name of the module to import
        clear_cache: Whether to clear module cache before import
        full_agent_import: If True, measure full Agent class import (recommended).
                          If False, measure package import only (misleading for Agno).
    
    Note: Agno's main __init__.py only exports __version__, so measuring 
    'import agno' gives misleading results (5ms). The actual Agent import
    'from agno.agent import Agent' takes ~500ms. This function measures
    the full Agent import by default for accurate comparison.
    """
    if clear_cache:
        # Clear module cache
        mods_to_remove = [k for k in sys.modules.keys() if module_name.split('.')[0] in k]
        for m in mods_to_remove:
            del sys.modules[m]
    
    gc.collect()
    start = time.perf_counter()
    
    if module_name == 'shadowbotagents':
        if full_agent_import:
            from shadowbotagents import Agent  # noqa: F401
        else:
            import shadowbotagents  # noqa: F401
    elif module_name == 'agno':
        if full_agent_import:
            from agno.agent import Agent  # noqa: F401
        else:
            import agno  # noqa: F401
    
    end = time.perf_counter()
    return (end - start) * 1000  # Return in milliseconds

def get_shadowbot_factory():
    """Get ShadowBot agent factory function."""
    from shadowbotagents import Agent
    
    def create():
        return Agent(name="Test", instructions="You are helpful.", output="silent")
    
    return create

def get_agno_factory():
    """Get Agno agent factory function."""
    try:
        from agno.agent import Agent as AgnoAgent
        
        def create():
            return AgnoAgent(name="Test", instructions=["You are helpful."])
        
        return create
    except ImportError:
        return None

def measure_instantiation(factory, iterations=50, warmup=5):
    """Measure agent instantiation time."""
    # Warmup
    for _ in range(warmup):
        factory()
    
    gc.collect()
    
    # Measure
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        factory()
        times.append((time.perf_counter() - start) * 1e6)  # microseconds
    
    return {
        'avg': sum(times) / len(times),
        'min': min(times),
        'max': max(times),
        'median': sorted(times)[len(times) // 2],
    }

def measure_memory(factory, iterations=20):
    """Measure memory footprint per agent."""
    import tracemalloc
    
    gc.collect()
    tracemalloc.start()
    
    agents = []
    for _ in range(iterations):
        agents.append(factory())
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    per_agent = current / iterations / 1024  # KB per agent
    return {
        'per_agent_kb': per_agent,
        'total_kb': current / 1024,
        'peak_kb': peak / 1024,
    }

def measure_function_calls(factory, iterations=50):
    """Count function calls using cProfile."""
    import cProfile
    import pstats
    from io import StringIO
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    for _ in range(iterations):
        factory()
    
    profiler.disable()
    
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    
    # Get total function calls
    total_calls = stats.total_calls
    calls_per_agent = total_calls / iterations
    
    # Get top functions by time
    stats.sort_stats('tottime')
    top_functions = []
    for func, (cc, nc, tt, ct, callers) in list(stats.stats.items())[:10]:
        filename, line, name = func
        top_functions.append({
            'name': name,
            'calls': nc,
            'tottime': tt * 1e6 / iterations,  # μs per agent
        })
    
    return {
        'total_calls': total_calls,
        'calls_per_agent': calls_per_agent,
        'top_functions': top_functions,
    }

def run_deep_profile(factory, iterations=50):
    """Run detailed cProfile analysis."""
    import cProfile
    import pstats
    from io import StringIO
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    for _ in range(iterations):
        factory()
    
    profiler.disable()
    
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(25)
    
    return stream.getvalue()

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive Quick Benchmark - ShadowBot vs Agno",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python benchmarks/quick_benchmark.py           # Standard benchmark
  python benchmarks/quick_benchmark.py --fast    # Quick mode
  python benchmarks/quick_benchmark.py --all     # All details
        """
    )
    parser.add_argument("--iterations", "-n", type=int, default=50,
                        help="Iterations for timing (default: 50)")
    parser.add_argument("--fast", "-f", action="store_true",
                        help="Fast mode (20 iterations)")
    parser.add_argument("--profile", "-p", action="store_true",
                        help="Show detailed cProfile output")
    parser.add_argument("--memory", "-m", action="store_true",
                        help="Show memory details")
    parser.add_argument("--import", dest="show_import", action="store_true",
                        help="Show import time details")
    parser.add_argument("--all", "-A", action="store_true",
                        help="Show all details")
    args = parser.parse_args()
    
    if args.fast:
        args.iterations = 20
    
    if args.all:
        args.profile = True
        args.memory = True
        args.show_import = True
    
    print("=" * 70)
    print("COMPREHENSIVE QUICK BENCHMARK - ShadowBot vs Agno")
    print("=" * 70)
    print(f"Iterations: {args.iterations}")
    print()
    
    results = {'shadowbot': {}, 'agno': {}}
    
    # ========================================================================
    # 1. IMPORT TIME
    # ========================================================================
    print("📦 Measuring import time...")
    
    results['shadowbot']['import_ms'] = measure_import_time('shadowbotagents')
    results['agno']['import_ms'] = measure_import_time('agno')
    
    # ========================================================================
    # 2. GET FACTORIES (after import measurement)
    # ========================================================================
    print("🏭 Loading factories...")
    
    shadowbot_factory = get_shadowbot_factory()
    agno_factory = get_agno_factory()
    
    if agno_factory is None:
        print("⚠️  Agno not installed, skipping comparison")
        return 1
    
    # ========================================================================
    # 3. INSTANTIATION TIME
    # ========================================================================
    print("⏱️  Measuring instantiation time...")
    
    results['shadowbot']['time'] = measure_instantiation(shadowbot_factory, args.iterations)
    results['agno']['time'] = measure_instantiation(agno_factory, args.iterations)
    
    # ========================================================================
    # 4. MEMORY FOOTPRINT
    # ========================================================================
    print("💾 Measuring memory footprint...")
    
    results['shadowbot']['memory'] = measure_memory(shadowbot_factory, min(args.iterations, 20))
    results['agno']['memory'] = measure_memory(agno_factory, min(args.iterations, 20))
    
    # ========================================================================
    # 5. FUNCTION CALLS
    # ========================================================================
    print("📊 Counting function calls...")
    
    results['shadowbot']['calls'] = measure_function_calls(shadowbot_factory, args.iterations)
    results['agno']['calls'] = measure_function_calls(agno_factory, args.iterations)
    
    # ========================================================================
    # RESULTS SUMMARY
    # ========================================================================
    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    
    # Import Time
    print()
    print("📦 IMPORT TIME (cold start)")
    print("-" * 50)
    print(f"{'Framework':<15} {'Time (ms)':<15} {'Relative':<15}")
    print("-" * 50)
    p_import = results['shadowbot']['import_ms']
    a_import = results['agno']['import_ms']
    print(f"{'ShadowBot':<15} {p_import:<15.2f} {'1.00x':<15}")
    print(f"{'Agno':<15} {a_import:<15.2f} {a_import/p_import:.2f}x")
    
    # Instantiation Time
    print()
    print("⏱️  INSTANTIATION TIME (per agent)")
    print("-" * 50)
    print(f"{'Framework':<15} {'Avg (μs)':<12} {'Min (μs)':<12} {'Median (μs)':<12}")
    print("-" * 50)
    p_time = results['shadowbot']['time']
    a_time = results['agno']['time']
    print(f"{'ShadowBot':<15} {p_time['avg']:<12.2f} {p_time['min']:<12.2f} {p_time['median']:<12.2f}")
    print(f"{'Agno':<15} {a_time['avg']:<12.2f} {a_time['min']:<12.2f} {a_time['median']:<12.2f}")
    
    ratio = p_time['avg'] / a_time['avg']
    diff = p_time['avg'] - a_time['avg']
    print()
    if ratio > 1:
        print(f"  → ShadowBot is {ratio:.2f}x slower ({diff:.2f}μs more)")
    else:
        print(f"  → ShadowBot is {1/ratio:.2f}x faster ({-diff:.2f}μs less)")
    
    # Memory
    print()
    print("💾 MEMORY FOOTPRINT (per agent)")
    print("-" * 50)
    print(f"{'Framework':<15} {'Per Agent (KB)':<15} {'Peak (KB)':<15}")
    print("-" * 50)
    p_mem = results['shadowbot']['memory']
    a_mem = results['agno']['memory']
    print(f"{'ShadowBot':<15} {p_mem['per_agent_kb']:<15.2f} {p_mem['peak_kb']:<15.2f}")
    print(f"{'Agno':<15} {a_mem['per_agent_kb']:<15.2f} {a_mem['peak_kb']:<15.2f}")
    
    # Function Calls
    print()
    print("📊 FUNCTION CALLS (per agent)")
    print("-" * 50)
    print(f"{'Framework':<15} {'Calls/Agent':<15} {'Total Calls':<15}")
    print("-" * 50)
    p_calls = results['shadowbot']['calls']
    a_calls = results['agno']['calls']
    print(f"{'ShadowBot':<15} {p_calls['calls_per_agent']:<15.1f} {p_calls['total_calls']:<15}")
    print(f"{'Agno':<15} {a_calls['calls_per_agent']:<15.1f} {a_calls['total_calls']:<15}")
    
    # ========================================================================
    # OVERALL SCORE
    # ========================================================================
    print()
    print("=" * 70)
    print("OVERALL COMPARISON")
    print("=" * 70)
    
    metrics = [
        ("Import Time", p_import, a_import, "lower"),
        ("Instantiation", p_time['avg'], a_time['avg'], "lower"),
        ("Memory/Agent", p_mem['per_agent_kb'], a_mem['per_agent_kb'], "lower"),
        ("Function Calls", p_calls['calls_per_agent'], a_calls['calls_per_agent'], "lower"),
    ]
    
    print(f"{'Metric':<20} {'ShadowBot':<15} {'Agno':<15} {'Winner':<15}")
    print("-" * 65)
    
    praison_wins = 0
    agno_wins = 0
    
    for name, p_val, a_val, better in metrics:
        if better == "lower":
            winner = "ShadowBot ✓" if p_val <= a_val else "Agno ✓"
            if p_val <= a_val:
                praison_wins += 1
            else:
                agno_wins += 1
        else:
            winner = "ShadowBot ✓" if p_val >= a_val else "Agno ✓"
            if p_val >= a_val:
                praison_wins += 1
            else:
                agno_wins += 1
        
        if isinstance(p_val, float):
            print(f"{name:<20} {p_val:<15.2f} {a_val:<15.2f} {winner:<15}")
        else:
            print(f"{name:<20} {p_val:<15} {a_val:<15} {winner:<15}")
    
    print("-" * 65)
    print(f"Score: ShadowBot {praison_wins} - Agno {agno_wins}")
    print("=" * 70)
    
    # ========================================================================
    # DETAILED OUTPUT (if requested)
    # ========================================================================
    
    if args.show_import:
        print()
        print("=" * 70)
        print("IMPORT TIME DETAILS")
        print("=" * 70)
        print(f"ShadowBot: {results['shadowbot']['import_ms']:.2f}ms")
        print(f"Agno: {results['agno']['import_ms']:.2f}ms")
    
    if args.memory:
        print()
        print("=" * 70)
        print("MEMORY DETAILS")
        print("=" * 70)
        print("ShadowBot:")
        print(f"  Per Agent: {p_mem['per_agent_kb']:.2f} KB")
        print(f"  Total: {p_mem['total_kb']:.2f} KB")
        print(f"  Peak: {p_mem['peak_kb']:.2f} KB")
        print("Agno:")
        print(f"  Per Agent: {a_mem['per_agent_kb']:.2f} KB")
        print(f"  Total: {a_mem['total_kb']:.2f} KB")
        print(f"  Peak: {a_mem['peak_kb']:.2f} KB")
    
    if args.profile:
        print()
        print("=" * 70)
        print("PRAISONAI DEEP PROFILE")
        print("=" * 70)
        print(run_deep_profile(shadowbot_factory, args.iterations))
        
        print()
        print("=" * 70)
        print("AGNO DEEP PROFILE")
        print("=" * 70)
        print(run_deep_profile(agno_factory, args.iterations))
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
