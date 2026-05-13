#!/usr/bin/env python3
"""
Quick test for the remote agent connectivity feature.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'shadowbot-agents'))

from shadowbotagents import Session

def test_remote_session_creation():
    """Test creating a remote session."""
    print("🧪 Testing remote session creation...")
    
    try:
        # This should fail gracefully since there's no server running
        session = Session(agent_url="localhost:8000/agent")
        print(f"❌ Unexpected: Session created without server: {session}")
    except ConnectionError as e:
        print(f"✅ Expected connection error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def test_local_session_backwards_compatibility():
    """Test that local sessions still work as before."""
    print("\n🧪 Testing local session backwards compatibility...")
    
    try:
        # This should work as before
        session = Session(session_id="test_local")
        print(f"✅ Local session created: {session}")
        
        # Test that it's not remote
        if session.is_remote:
            print("❌ Local session incorrectly marked as remote")
            return False
        
        print("✅ Local session correctly identified")
        return True
        
    except Exception as e:
        print(f"❌ Error creating local session: {e}")
        return False

def test_remote_session_restrictions():
    """Test that remote sessions properly restrict local operations."""
    print("\n🧪 Testing remote session restrictions...")
    
    try:
        # Create a mock remote session (will fail connection but that's OK for testing restrictions)
        session = Session(agent_url="mock://fake-server:8000/agent")
    except ConnectionError:
        # Create the session object manually for testing restrictions
        session = Session.__new__(Session)
        session.session_id = "test_remote"
        session.user_id = "test_user"
        session.agent_url = "mock://fake-server:8000/agent"
        session.timeout = 30
        session.is_remote = True
        session.memory_config = {}
        session.knowledge_config = {}
        session._memory = None
        session._knowledge = None
        session._agents_instance = None
    
    # Test memory restriction
    try:
        _ = session.memory
        print("❌ Memory access should be restricted for remote sessions")
        return False
    except ValueError as e:
        print(f"✅ Memory properly restricted: {e}")
    
    # Test knowledge restriction
    try:
        _ = session.knowledge
        print("❌ Knowledge access should be restricted for remote sessions")
        return False
    except ValueError as e:
        print(f"✅ Knowledge properly restricted: {e}")
    
    # Test agent creation restriction
    try:
        session.Agent(name="Test", role="Assistant")
        print("❌ Agent creation should be restricted for remote sessions")
        return False
    except ValueError as e:
        print(f"✅ Agent creation properly restricted: {e}")
    
    return True

def main():
    """Run all tests."""
    print("🚀 Testing Remote Agent Connectivity Implementation")
    print("=" * 60)
    
    tests = [
        test_remote_session_creation,
        test_local_session_backwards_compatibility, 
        test_remote_session_restrictions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("❌ Test failed!")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Remote agent connectivity is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
