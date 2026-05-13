from shadowbot import ShadowBot
from duckduckgo_search import DDGS
from shadowbot_tools import BaseTool

class InternetSearchTool(BaseTool):
    name: str = "InternetSearchTool"
    description: str = "Search Internet for relevant information based on a query or latest news"

    def _run(self, query: str):
        ddgs = DDGS()
        results = ddgs.text(keywords=query, region='wt-wt', safesearch='moderate', max_results=5)
        return results

# Example agent_yaml content
agent_yaml = """
framework: "crewai"
topic: "Space Exploration"

roles:
  astronomer:
    role: "Space Researcher"
    goal: "Discover new insights about {topic}"
    backstory: "You are a curious and dedicated astronomer with a passion for unraveling the mysteries of the cosmos."
    tasks:
      investigate_exoplanets:
        description: "Research and compile information about exoplanets discovered in the last decade."
        expected_output: "A summarized report on exoplanet discoveries, including their size, potential habitability, and distance from Earth."
    tools:
      - "InternetSearchTool"
"""

# Create a ShadowBot instance with the agent_yaml content
shadowbot = ShadowBot(agent_yaml=agent_yaml)

# Run ShadowBot
result = shadowbot.run()

# Print the result
print(result)