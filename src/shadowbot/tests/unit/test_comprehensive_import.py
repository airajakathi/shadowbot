#!/usr/bin/env python3
"""
Comprehensive test script to verify all import scenarios work correctly
Tests the original failing import from the GitHub issue
"""

import sys
import os

# Add the shadowbot-agents source to Python path
sys.path.insert(0, '/home/runner/work/ShadowBot/ShadowBot/src/shadowbot-agents')

def test_original_failing_import():
    """Test the exact import that was failing in the GitHub issue"""
    print("=== Testing Original Failing Import ===")
    try:
        from shadowbotagents.agents.agents import Agent, Task, Agents
        print('✅ SUCCESS: from shadowbotagents.agents.agents import Agent, Task, Agents')
        return True
    except ImportError as e:
        print(f'❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f'❌ UNEXPECTED ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_memory_direct_import():
    """Test direct Memory import"""
    print("\n=== Testing Direct Memory Import ===")
    try:
        from shadowbotagents.memory import Memory
        print('✅ SUCCESS: from shadowbotagents.memory import Memory')
        return True
    except ImportError as e:
        print(f'❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f'❌ UNEXPECTED ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_memory_from_package_root():
    """Test Memory import from package root"""
    print("\n=== Testing Memory Import from Package Root ===")
    try:
        from shadowbotagents import Memory
        print('✅ SUCCESS: from shadowbotagents import Memory')
        return True
    except ImportError as e:
        print(f'❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f'❌ UNEXPECTED ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_session_import():
    """Test Session import which depends on Memory"""
    print("\n=== Testing Session Import ===")
    try:
        from shadowbotagents.session import Session
        print('✅ SUCCESS: from shadowbotagents.session import Session')
        return True
    except ImportError as e:
        print(f'❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f'❌ UNEXPECTED ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_memory_instantiation():
    """Test that Memory can be instantiated without errors"""
    print("\n=== Testing Memory Instantiation ===")
    try:
        from shadowbotagents.memory import Memory
        
        # Test with minimal config (no external dependencies)
        config = {"provider": "none"}
        memory = Memory(config=config)
        print('✅ SUCCESS: Memory instance created with provider="none"')
        
        # Test basic methods don't fail immediately
        memory.store_short_term("test content", metadata={"test": True})
        results = memory.search_short_term("test", limit=1)
        print('✅ SUCCESS: Basic memory operations work')
        
        return True
    except Exception as e:
        print(f'❌ ERROR: {e}')
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("🔍 Running comprehensive import tests...")
    
    tests = [
        test_original_failing_import,
        test_memory_direct_import, 
        test_memory_from_package_root,
        test_session_import,
        test_memory_instantiation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 ALL TESTS PASSED! The Memory import issue has been resolved.")
    else:
        print("❌ Some tests failed. The issue may not be fully resolved.")
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
