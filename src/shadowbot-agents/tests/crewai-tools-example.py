# example tools.py
from duckduckgo_search import DDGS
from shadowbot_tools import BaseTool

class InternetSearchTool(BaseTool):
    name: str = "InternetSearchTool"
    description: str = "Search Internet for relevant information based on a query or latest news"

    def _run(self, query: str):
        ddgs = DDGS()
        results = ddgs.text(keywords=query, region='wt-wt', safesearch='moderate', max_results=5)
        return results

# Example agent
from shadowbotagents import Agent
from shadowbotagents import AgentTeam
agent = Agent(
    name="Internet Search Agent",
    tools=[InternetSearchTool],
    instructions="""
    You are an agent that can search the internet for relevant information based on a query or latest news.
    """
)

# Run the agent
result = AgentTeam(agents=[agent], verbose=10).start()
print(result)
