from google.adk.agents import Agent, LoopAgent, SequentialAgent
from agent.tools import web_search
import os

from agent.prompts import (
    query_writer_instructions,
    reflection_instructions,
    answer_instructions,
)


# Query generation agent
# This agent will be responsible for generating the initial search queries.
query_generation_agent = Agent(
    name="query_generation_agent",
    model=os.getenv("REASONING_MODEL", "gemini-1.5-flash-latest"),
    instruction=query_writer_instructions,
    description="This agent generates search queries to answer the user's question.",
)

# Research agent
# This agent will be responsible for conducting web research.
# It uses the web_search tool to search the web and gather information.
research_agent = Agent(
    name="research_agent",
    model=os.getenv("REASONING_MODEL", "gemini-1.5-flash-latest"),
    instruction="You are a research assistant. Your goal is to answer the user's question by conducting web research.",
    description="This agent conducts web research to answer the user's question.",
    tools=[web_search],
)

# Research loop agent
# This agent will loop through the research process until the user's question is answered.
research_loop = LoopAgent(
    agent=research_agent,
    name="research_loop",
    description="This agent loops through the research process until the user's question is answered.",
    max_iterations=3,
)

# Reflection agent
# This agent will analyze the research results and determine if more information is needed.
reflection_agent = Agent(
    name="reflection_agent",
    model=os.getenv("REASONING_MODEL", "gemini-1.5-flash-latest"),
    instruction=reflection_instructions,
    description="This agent analyzes the research results and determines if more information is needed.",
)

# Answer agent
# This agent will generate the final answer based on the research.
answer_agent = Agent(
    name="answer_agent",
    model=os.getenv("REASONING_MODEL", "gemini-1.5-flash-latest"),
    instruction=answer_instructions,
    description="This agent generates the final answer based on the research.",
)

# Root agent
# This agent will orchestrate the other agents in a sequence.
root_agent = SequentialAgent(
    name="pro_search_agent",
    description="This agent orchestrates the research process to answer the user's question.",
    agents=[
        query_generation_agent,
        research_loop,
        reflection_agent,
        answer_agent,
    ],
)
