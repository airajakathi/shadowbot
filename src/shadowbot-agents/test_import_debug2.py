#!/usr/bin/env python3
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
# Add the shadowbot-agents directory to the path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'shadowbot-agents'))

print("Testing import functionality...")

# Check if shadowbot is found
try:
    import shadowbot
    print(f"✓ shadowbot package found at: {shadowbot.__file__}")
    print(f"shadowbot.__path__: {shadowbot.__path__}")
    print(f"shadowbot dir: {dir(shadowbot)}")
except Exception as e:
    print(f"Error importing shadowbot: {e}")

# Check shadowbot.shadowbot
try:
    import shadowbot.shadowbot
    print(f"✓ shadowbot.shadowbot package found at: {shadowbot.shadowbot.__file__}")
    print(f"shadowbot.shadowbot dir: {dir(shadowbot.shadowbot)}")
    if hasattr(shadowbot.shadowbot, '__all__'):
        print(f"shadowbot.shadowbot.__all__: {shadowbot.shadowbot.__all__}")
    
    # Check what we can actually import
    print("\nTesting actual imports from shadowbot.shadowbot:")
    for symbol in ['ShadowBot', '__version__', 'Agent', 'Task', 'ShadowBotAgents']:
        if hasattr(shadowbot.shadowbot, symbol):
            print(f"✓ {symbol} is available")
        else:
            print(f"❌ {symbol} is NOT available")
            
except Exception as e:
    print(f"Error importing shadowbot.shadowbot: {e}")

# Test direct import
try:
    from shadowbot.shadowbot import ShadowBot, __version__
    print(f"✓ Direct import from shadowbot.shadowbot works: ShadowBot={ShadowBot}, __version__={__version__}")
except Exception as e:
    print(f"❌ Direct import from shadowbot.shadowbot failed: {e}")

# Test import from shadowbotagents
print("\nTesting shadowbotagents:")
try:
    import shadowbotagents
    print(f"✓ shadowbotagents is available: {shadowbotagents}")
    print(f"shadowbotagents.__all__: {shadowbotagents.__all__}")
except Exception as e:
    print(f"❌ shadowbotagents import failed: {e}")