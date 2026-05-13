"""Example: Discover tools from installed packages."""

# Discover from shadowbotagents built-in tools
try:
    from shadowbotagents.tools import TOOL_MAPPINGS
    print("Built-in tools from shadowbotagents:")
    for name in list(TOOL_MAPPINGS.keys())[:10]:
        print(f"  - {name}")
    print(f"  ... and {len(TOOL_MAPPINGS) - 10} more")
except ImportError:
    print("shadowbotagents not installed")

# Discover from shadowbot_tools
try:
    import shadowbot_tools
    print("\nTools from shadowbot_tools:")
    
    # Check for video module
    try:
        from shadowbot_tools import video
        print("  - shadowbot_tools.video (video editing)")
    except ImportError:
        pass
except ImportError:
    print("shadowbot_tools not installed")
