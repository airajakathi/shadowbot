#!/usr/bin/env python3
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
# Add the shadowbot-agents directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'shadowbot-agents'))

print("Testing import functionality...")

try:
    import shadowbotagents
    print("✓ shadowbotagents module is available")
    
    # Test importing specific classes
    try:
        from shadowbotagents import Agent, Task, AgentTeam
        print("✓ Successfully imported Agent, Task, AgentManager from shadowbotagents")
    except ImportError as e:
        print(f"❌ Failed to import specific classes: {e}")
        
except ImportError as e:
    print(f"❌ shadowbotagents module not available: {e}")

# Test the shadowbot package
try:
    import shadowbot
    print("✓ shadowbot package is available")
    
    # Test importing from shadowbot
    try:
        from shadowbot import Agent, Task, AgentManager
        print("✓ Successfully imported Agent, Task, AgentManager from shadowbot")
    except ImportError as e:
        print(f"❌ Failed to import from shadowbot: {e}")
        
except ImportError as e:
    print(f"❌ shadowbot package not available: {e}")

# Check what's in the shadowbot package
try:
    import shadowbot
    print(f"shadowbot package contents: {dir(shadowbot)}")
    if hasattr(shadowbot, '__all__'):
        print(f"shadowbot.__all__: {shadowbot.__all__}")
    
    # Check what we can actually import
    print("\nTesting actual imports:")
    for symbol in ['ShadowBot', '__version__', 'Agent', 'Task', 'Agents']:
        if hasattr(shadowbot, symbol):
            print(f"✓ {symbol} is available")
        else:
            print(f"❌ {symbol} is NOT available")
            
except Exception as e:
    print(f"Error checking shadowbot package: {e}")