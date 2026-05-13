from shadowbot import ShadowBot
import os
    
def advanced_agent_example():
    # Get the correct path to agents.yaml relative to the test file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    agent_file_path = os.path.join(current_dir, "agents.yaml")
    
    # For fast tests, we don't actually run the LLM calls
    # Just verify that ShadowBot can be instantiated properly with autogen
    try:
        shadowbot = ShadowBot(
            agent_file=agent_file_path,
            framework="autogen",
        )
        print(shadowbot)
        # Return success without making actual API calls
        return "Advanced example setup completed successfully"
    except Exception as e:
        return f"Advanced example failed during setup: {e}"

def advanced():
    return advanced_agent_example()

if __name__ == "__main__":
    print(advanced())