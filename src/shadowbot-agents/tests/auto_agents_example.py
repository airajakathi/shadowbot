from shadowbotagents import AutoAgents
from shadowbotagents.tools import duckduckgo

agents = AutoAgentTeam(
    instructions="Search for information about AI Agents",
    tools=[duckduckgo],
    process="sequential",
    verbose=True
)

agents.start()