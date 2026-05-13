#!/usr/bin/env python3

print("Testing syntax fix...")

try:
    # Test basic import
    import ast
    
    # Parse the agent.py file to check for syntax errors
    with open('shadowbotagents/agent/agent.py', 'r') as f:
        content = f.read()
    
    # This will raise SyntaxError if there are issues
    ast.parse(content)
    print("✅ agent.py syntax is valid")
    
    # Test actual import
    from shadowbotagents.agent.agent import Agent
    print("✅ Agent import successful")
    
    print("🎉 All syntax checks passed!")
    
except SyntaxError as e:
    print(f"❌ Syntax error: {e}")
    print(f"   Line {e.lineno}: {e.text}")
    exit(1)
except Exception as e:
    print(f"❌ Import error: {e}")
    exit(1) 