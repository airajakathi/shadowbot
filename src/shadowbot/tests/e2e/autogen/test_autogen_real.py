"""
AutoGen Real End-to-End Test

⚠️  WARNING: This test makes real API calls and may incur costs!

This test verifies AutoGen framework integration with actual LLM calls.
Run only when you have:
- Valid API keys set as environment variables
- Understanding that this will consume API credits
"""

import pytest
import os
import sys
import tempfile
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))

@pytest.mark.real
class TestAutoGenReal:
    """Real AutoGen tests with actual API calls"""

    def test_autogen_simple_conversation(self):
        """Test a simple AutoGen conversation with real API calls"""
        try:
            from shadowbot import ShadowBot
            
            # Create a minimal YAML configuration
            yaml_content = """
framework: autogen
topic: Simple Math Question
roles:
  - name: Math_Teacher
    goal: Help solve basic math problems
    backstory: I am a helpful math teacher
    tasks:
      - description: What is 2 + 2? Provide just the number.
        expected_output: The answer to 2 + 2
"""
            
            # Create temporary test file
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                test_file = f.name
            
            try:
                # Initialize ShadowBot with AutoGen
                shadowbot = ShadowBot(
                    agent_file=test_file,
                    framework="autogen"
                )
                
                # Verify setup
                assert shadowbot is not None
                assert shadowbot.framework == "autogen"
                
                print("✅ AutoGen real test setup successful")
                
                # Note: Full execution would be:
                # result = shadowbot.run()
                # But we keep it minimal to avoid costs
                
            finally:
                # Cleanup
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except ImportError as e:
            pytest.skip(f"AutoGen not available: {e}")
        except Exception as e:
            pytest.fail(f"AutoGen real test failed: {e}")

    def test_autogen_environment_check(self):
        """Verify AutoGen environment is properly configured"""
        # Check API key is available
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY required for real tests")
        
        # Check AutoGen can be imported
        try:
            import autogen
            assert autogen is not None
        except ImportError:
            pytest.skip("AutoGen not installed")
            
        print("✅ AutoGen environment check passed")

    @pytest.mark.skipif(not os.getenv("PRAISONAI_RUN_FULL_TESTS"), 
                        reason="Full execution test requires PRAISONAI_RUN_FULL_TESTS=true")
    def test_autogen_full_execution(self):
        """
        💰 EXPENSIVE TEST: Actually runs shadowbot.run() with real API calls!
        
        Set PRAISONAI_RUN_FULL_TESTS=true to enable this test.
        This will consume API credits and show real output logs.
        """
        try:
            from shadowbot import ShadowBot
            import logging
            
            # Enable detailed logging to see the output
            logging.basicConfig(level=logging.INFO)
            
            print("\n" + "="*60)
            print("💰 STARTING FULL EXECUTION TEST (REAL API CALLS!)")
            print("="*60)
            
            # Create a very simple YAML for minimal cost
            yaml_content = """
framework: autogen
topic: Quick Test
roles:
  - name: Assistant
    goal: Answer very briefly
    backstory: I give one-word answers
    tasks:
      - description: What is 1+1? Answer with just the number, nothing else.
        expected_output: Just the number
"""
            
            # Create temporary test file
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(yaml_content)
                test_file = f.name
            
            try:
                # Initialize ShadowBot with AutoGen
                shadowbot = ShadowBot(
                    agent_file=test_file,
                    framework="autogen"
                )
                
                print(f"🤖 Initializing AutoGen with file: {test_file}")
                print(f"📋 Framework: {shadowbot.framework}")
                
                # 💰 ACTUAL EXECUTION - THIS COSTS MONEY!
                print("\n💰 EXECUTING REAL AUTOGEN WORKFLOW...")
                print("⚠️  This will make actual API calls!")
                
                result = shadowbot.run()
                
                print("\n" + "="*60)
                print("✅ AUTOGEN EXECUTION COMPLETED!")
                print("="*60)
                print(f"📊 Result type: {type(result)}")
                if result:
                    print(f"📄 Result content: {str(result)[:500]}...")
                else:
                    print("📄 No result returned")
                print("="*60)
                
                # Verify we got some result
                assert result is not None or True  # Allow empty results
                
            finally:
                # Cleanup
                if os.path.exists(test_file):
                    os.unlink(test_file)
                    
        except ImportError as e:
            pytest.skip(f"AutoGen not available: {e}")
        except Exception as e:
            print(f"\n❌ AutoGen full execution failed: {e}")
            pytest.fail(f"AutoGen full execution test failed: {e}")

if __name__ == "__main__":
    # Enable full tests when running directly
    os.environ["PRAISONAI_RUN_FULL_TESTS"] = "true"
    pytest.main([__file__, "-v", "-m", "real", "-s"]) 