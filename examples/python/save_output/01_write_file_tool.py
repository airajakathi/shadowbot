"""
Example 1: Save Agent Output Using write_file Tool

The agent decides when and what to save based on the task.
"""

from shadowbotagents import Agent
from shadowbotagents.tools import write_file

# Create agent with write_file tool
agent = Agent(
    name="ContentWriter",
    role="Technical Writer",
    goal="Create and save technical documentation",
    tools=[write_file]
)

# Agent will use write_file tool to save the content
result = agent.start("Write a short poem about coding and save it to poem.txt")

print("✅ Task completed!")
print(f"Result: {result}")
