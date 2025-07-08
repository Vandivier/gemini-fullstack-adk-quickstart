from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="pro_search_agent",
    model="gemini-2.0-flash",
    instruction=(
        "You are a helpful research assistant. First, understand the user's question. "
        "Then, use Google Search to find relevant, up-to-date information. "
        "Finally, synthesize the information into a clear and concise answer. "
        "You must cite your sources."
    ),
    description="An agent that can answer questions by searching the web.",
    tools=[google_search],
)
