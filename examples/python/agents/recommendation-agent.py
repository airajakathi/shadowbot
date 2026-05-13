from shadowbotagents import Agent, Tools
from shadowbotagents.tools import duckduckgo

agent = Agent(instructions="You are a Recommendation Agent", tools=[duckduckgo])
agent.start("Recommend me a good movie to watch in 2025")