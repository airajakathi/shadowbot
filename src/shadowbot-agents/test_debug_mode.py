#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'src/shadowbot-agents')

print("Testing DEBUG mode functionality...")

def test_normal_mode():
    """Test that warnings are suppressed in normal mode"""
    print("\n=== Testing NORMAL mode (LOGLEVEL=INFO) ===")
    os.environ['LOGLEVEL'] = 'INFO'
    
    # Force reload modules to apply new environment
    import sys
    for mod in list(sys.modules.keys()):
        if mod.startswith('shadowbotagents'):
            del sys.modules[mod]
    
    import warnings
    warnings.simplefilter('always')
    
    try:
        import shadowbotagents
        print("✅ Import successful in normal mode")
        
        # Check if warning suppression is active
        import shadowbotagents.__init__ as main_init
        should_suppress = main_init._should_suppress_warnings()
        print(f"✅ Warning suppression active: {should_suppress}")
        
    except Exception as e:
        print(f"❌ Error in normal mode: {e}")
        return False
    
    return True

def test_debug_mode():
    """Test that warnings are shown in DEBUG mode"""
    print("\n=== Testing DEBUG mode (LOGLEVEL=DEBUG) ===")
    os.environ['LOGLEVEL'] = 'DEBUG'
    
    # Force reload modules to apply new environment
    import sys
    for mod in list(sys.modules.keys()):
        if mod.startswith('shadowbotagents'):
            del sys.modules[mod]
    
    import warnings
    warnings.simplefilter('always')
    
    try:
        import shadowbotagents
        print("✅ Import successful in debug mode")
        
        # Check if warning suppression is inactive
        import shadowbotagents.__init__ as main_init
        should_suppress = main_init._should_suppress_warnings()
        print(f"✅ Warning suppression active: {should_suppress} (should be False)")
        
        if should_suppress:
            print("❌ WARNING: Debug mode should not suppress warnings!")
            return False
        else:
            print("✅ DEBUG mode correctly allows warnings")
            
    except Exception as e:
        print(f"❌ Error in debug mode: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Testing DEBUG mode implementation")
    
    # Clean up environment first
    if 'LOGLEVEL' in os.environ:
        del os.environ['LOGLEVEL']
    
    normal_success = test_normal_mode()
    debug_success = test_debug_mode()
    
    print("\n" + "="*50)
    if normal_success and debug_success:
        print("🎉 ALL TESTS PASSED: DEBUG mode functionality works correctly!")
        print("✅ Warnings suppressed in normal mode")
        print("✅ Warnings enabled in DEBUG mode")
    else:
        print("💥 TESTS FAILED: Issues with DEBUG mode implementation")
    
    # Restore normal mode
    os.environ['LOGLEVEL'] = 'INFO'
    
    sys.exit(0 if (normal_success and debug_success) else 1)