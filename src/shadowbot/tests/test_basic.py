#!/usr/bin/env python3

print("🧪 Basic Python Test")
print("=" * 20)

# Test basic imports
try:
    import sys
    print(f"✅ Python version: {sys.version}")
    print(f"✅ Python executable: {sys.executable}")
except Exception as e:
    print(f"❌ Basic imports failed: {e}")

# Test shadowbotagents import
try:
    import sys
    sys.path.insert(0, 'src')
    import shadowbotagents
    print("✅ shadowbotagents import: SUCCESS")
except Exception as e:
    print(f"❌ shadowbotagents import failed: {e}")

# Test legacy example
try:
    sys.path.insert(0, 'tests')
    from basic_example import basic_agent_example
    result = basic_agent_example()
    print(f"✅ basic_example result: {result}")
except Exception as e:
    print(f"❌ basic_example failed: {e}")

print("\n🎉 Basic test completed!") 