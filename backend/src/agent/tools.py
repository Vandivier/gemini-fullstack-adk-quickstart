import os

from google.genai import Client
from agent.prompts import web_searcher_instructions, get_current_date
from agent.utils import (
    get_citations,
    insert_citation_markers,
    resolve_urls,
)

# Used for Google Search API
genai_client = Client(api_key=os.getenv("GEMINI_API_KEY"))


def web_search(search_query: str, id: int = 0) -> dict:
    """Performs web research using the native Google Search API tool.

    Executes a web search using the native Google Search API tool in combination with Gemini Flash.

    Args:
        search_query: The search query to use for the web search.
        id: A unique id for the search query.

    Returns:
        A dictionary containing the search results, including the modified text and the sources gathered.
    """
    # Configure
    formatted_prompt = web_searcher_instructions.format(
        current_date=get_current_date(),
        research_topic=search_query,
    )

    # Uses the google genai client as the langchain client doesn't return grounding metadata
    response = genai_client.models.generate_content(
        model=os.getenv("REASONING_MODEL", "gemini-1.5-flash-latest"),
        contents=formatted_prompt,
        config={
            "tools": [{"google_search": {}}],
            "temperature": 0,
        },
    )
    # resolve the urls to short urls for saving tokens and time
    resolved_urls = resolve_urls(
        response.candidates[0].grounding_metadata.grounding_chunks, id
    )
    # Gets the citations and adds them to the generated text
    citations = get_citations(response, resolved_urls)
    modified_text = insert_citation_markers(response.text, citations)
    sources_gathered = [item for citation in citations for item in citation["segments"]]

    return {
        "sources_gathered": sources_gathered,
        "search_query": search_query,
        "web_research_result": modified_text,
    }
