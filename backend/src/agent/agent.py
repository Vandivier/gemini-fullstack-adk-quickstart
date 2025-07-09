from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool, google_search

from .tools import roll_dice


# Define the agent for custom tools (rolling dice)
agent_custom_tools = LlmAgent(
    name="dice_roller_agent",
    model="gemini-2.0-flash",
    instruction="You are a specialist in rolling dice. Use the `roll_dice` tool to fulfill the user's request.",
    description="An agent that specializes in rolling dice (e.g., 'roll a d20', 'roll 2d6').",
    tools=[roll_dice],
)

# Define the agent for built-in tools (web search)
agent_built_in_tools = LlmAgent(
    name="search_agent",
    model="gemini-2.0-flash",
    instruction="You are a specialist in searching the web. Use the `google_search` tool to find information.",
    description="An agent that can answer questions by searching the web.",
    tools=[google_search],
)

# Define the root agent that uses the specialist agents as tools.
root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.0-flash",
    instruction=(
        "You are a master assistant that uses tools to answer questions.\n"
        "To roll dice, use the `dice_roller_agent` tool.\n"
        "To answer questions that require web search, use the `search_agent` tool."
    ),
    description="A root agent that uses specialist agents as tools.",
    # using tools instead of sub_agents is a workaround for a bug in the ADK
    # see https://github.com/google/adk-python/issues/53#issuecomment-2798906767
    # and https://google.github.io/adk-docs/agents/multi-agents/
    tools=[
        agent_tool.AgentTool(agent=agent_custom_tools),
        agent_tool.AgentTool(agent=agent_built_in_tools),
    ],
)
