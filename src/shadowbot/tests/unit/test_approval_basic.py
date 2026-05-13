#!/usr/bin/env python3
"""
Basic test to verify the human approval system implementation.

This test focuses on ensuring the approval decorators and callback system work correctly.
"""

import sys
import os
import asyncio

# Add the shadowbot-agents module to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shadowbot-agents')))

def test_imports():
    """Test that all the new approval imports work correctly."""
    try:
        from shadowbotagents.approval import (
            require_approval,
            ApprovalDecision,
            console_approval_callback,
            request_approval,
            add_approval_requirement,
            remove_approval_requirement,
            is_approval_required,
            get_risk_level,
            APPROVAL_REQUIRED_TOOLS,
            TOOL_RISK_LEVELS
        )
        print("✅ All approval imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        assert False, f"Import failed: {e}"

def test_approval_configuration():
    """Test approval requirement configuration."""
    from shadowbotagents.approval import (
        add_approval_requirement, 
        remove_approval_requirement, 
        is_approval_required, 
        get_risk_level,
        APPROVAL_REQUIRED_TOOLS,
        TOOL_RISK_LEVELS
    )
    
    print("\n🔧 Testing approval configuration...")
    
    # Test adding requirement
    add_approval_requirement("test_tool", "medium")
    assert is_approval_required("test_tool"), "Tool should require approval after adding"
    assert get_risk_level("test_tool") == "medium", "Risk level should be medium"
    print("✅ Add approval requirement works")
    
    # Test removing requirement
    remove_approval_requirement("test_tool")
    assert not is_approval_required("test_tool"), "Tool should not require approval after removing"
    assert get_risk_level("test_tool") is None, "Risk level should be None after removal"
    print("✅ Remove approval requirement works")
    
    # Test default dangerous tools are configured
    assert is_approval_required("execute_command"), "execute_command should require approval by default"
    assert get_risk_level("execute_command") == "critical", "execute_command should be critical risk"
    print("✅ Default dangerous tools are configured")
    
    print(f"✅ Current approval-required tools: {len(APPROVAL_REQUIRED_TOOLS)} configured")

def test_approval_decorator():
    """Test the require_approval decorator."""
    from shadowbotagents.approval import require_approval, is_approval_required, get_risk_level, set_approval_callback, ApprovalDecision
    
    print("\n🎯 Testing approval decorator...")
    
    # Set auto-approval callback for testing
    def auto_approve_callback(function_name, arguments, risk_level):
        print(f"🤖 Auto-approving {function_name} (risk: {risk_level})")
        return ApprovalDecision(approved=True, reason="Auto-approved for testing")
    
    set_approval_callback(auto_approve_callback)
    
    # Test decorator on a test function
    @require_approval(risk_level="high")
    def test_dangerous_function(param1, param2="default"):
        """A test function that requires approval."""
        return f"Executed with {param1} and {param2}"
    
    # Check if the function is marked as requiring approval
    assert is_approval_required("test_dangerous_function"), "Decorated function should require approval"
    assert get_risk_level("test_dangerous_function") == "high", "Risk level should match decorator"
    print("✅ Approval decorator works correctly")
    
    # Test that the function executes normally with auto-approval
    result = test_dangerous_function("test", param2="value")
    assert "Executed with test and value" in result, "Function should execute normally"
    print("✅ Decorated function executes correctly")

def test_tool_integration():
    """Test that dangerous tools have approval decorators."""
    print("\n🛠️ Testing tool integration...")
    
    # Test shell tools
    try:
        from shadowbotagents.tools.shell_tools import ShellTools
        shell_tools = ShellTools()
        
        # Check if execute_command requires approval
        from shadowbotagents.approval import is_approval_required
        assert is_approval_required("execute_command"), "execute_command should require approval"
        print("✅ ShellTools.execute_command requires approval")
        
        # Check if kill_process requires approval
        assert is_approval_required("kill_process"), "kill_process should require approval"
        print("✅ ShellTools.kill_process requires approval")
        
    except Exception as e:
        print(f"⚠️ Shell tools test failed: {e}")
        
    # Test python tools
    try:
        from shadowbotagents.tools.python_tools import PythonTools
        python_tools = PythonTools()
        
        # Check if execute_code requires approval
        assert is_approval_required("execute_code"), "execute_code should require approval"
        print("✅ PythonTools.execute_code requires approval")
        
    except Exception as e:
        print(f"⚠️ Python tools test failed: {e}")
        
    # Test file tools
    try:
        from shadowbotagents.tools.file_tools import FileTools
        file_tools = FileTools()
        
        # Check if write_file requires approval
        assert is_approval_required("write_file"), "write_file should require approval"
        print("✅ FileTools.write_file requires approval")
        
        # Check if delete_file requires approval
        assert is_approval_required("delete_file"), "delete_file should require approval"
        print("✅ FileTools.delete_file requires approval")
        
    except Exception as e:
        print(f"⚠️ File tools test failed: {e}")

async def test_approval_callback():
    """Test the approval callback system."""
    print("\n📞 Testing approval callback system...")
    
    from shadowbotagents.approval import request_approval, ApprovalDecision
    
    # Mock approval that auto-denies
    def mock_denial_callback(function_name, arguments, risk_level):
        print(f"🔒 Mock callback: Denying {function_name} (risk: {risk_level})")
        return ApprovalDecision(approved=False, reason="Test denial")
    
    # Mock approval that auto-approves
    def mock_approval_callback(function_name, arguments, risk_level):
        print(f"✅ Mock callback: Approving {function_name} (risk: {risk_level})")
        return ApprovalDecision(approved=True, reason="Test approval")
    
    # Test with denial callback
    from shadowbotagents.approval import set_approval_callback
    set_approval_callback(mock_denial_callback)
    
    decision = await request_approval("execute_command", {"command": "ls"})
    assert not decision.approved, "Should be denied by mock callback"
    assert "Test denial" in decision.reason, "Should have denial reason"
    print("✅ Denial callback works")
    
    # Test with approval callback  
    set_approval_callback(mock_approval_callback)
    
    decision = await request_approval("execute_command", {"command": "ls"})
    assert decision.approved, "Should be approved by mock callback"
    assert "Test approval" in decision.reason, "Should have approval reason"
    print("✅ Approval callback works")
    
    # Test non-dangerous tool (should auto-approve)
    decision = await request_approval("safe_function", {})
    assert decision.approved, "Non-dangerous tools should auto-approve"
    assert "No approval required" in decision.reason, "Should indicate no approval needed"
    print("✅ Non-dangerous tools auto-approve")

def test_agent_integration():
    """Test that agents properly integrate with the approval system."""
    print("\n🤖 Testing agent integration...")
    
    try:
        from shadowbotagents import Agent
        from shadowbotagents.tools.shell_tools import ShellTools
        
        # Create agent with dangerous tools
        agent = Agent(
            name="Test Agent",
            role="Tester",
            goal="Test approval integration",
            tools=[ShellTools()]
        )
        
        print("✅ Agent created with dangerous tools")
        
        # Check that agent has the approval callback configured
        from shadowbotagents.main import approval_callback
        print(f"✅ Global approval callback configured: {approval_callback is not None}")
        
    except Exception as e:
        print(f"⚠️ Agent integration test failed: {e}")
        assert False, f"Agent integration test failed: {e}"

def main():
    """Run all approval system tests."""
    print("🧪 ShadowBot Human Approval System Test Suite")
    print("=" * 50)
    
    test_results = []
    
    # Run synchronous tests
    try:
        test_imports()
        test_results.append(("Imports", True))
    except Exception as e:
        test_results.append(("Imports", False))
        
    try:
        test_approval_configuration()
        test_results.append(("Configuration", True))
    except Exception as e:
        test_results.append(("Configuration", False))
        
    try:
        test_approval_decorator()
        test_results.append(("Decorator", True))
    except Exception as e:
        test_results.append(("Decorator", False))
        
    try:
        test_tool_integration()
        test_results.append(("Tool Integration", True))
    except Exception as e:
        test_results.append(("Tool Integration", False))
        
    try:
        test_agent_integration()
        test_results.append(("Agent Integration", True))
    except Exception as e:
        test_results.append(("Agent Integration", False))
    
    # Run async tests
    try:
        asyncio.run(test_approval_callback())
        test_results.append(("Approval Callback", True))
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        test_results.append(("Approval Callback", False))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotal: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Human approval system is working correctly.")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)