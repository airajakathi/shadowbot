from shadowbotagents import Agent, Tools
from shadowbotagents.tools import duckduckgo

agent = Agent(instructions="You are a Research Agent", tools=[duckduckgo])
agent.start("Research about AI 2024")