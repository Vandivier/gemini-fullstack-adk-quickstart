# mypy: disable - error - code = "no-untyped-def,misc"
import pathlib
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runners import InMemoryRunner
from agent import root_agent
import json

# Define the FastAPI app
app = FastAPI()

# Add CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173",
        "http://localhost:3000",
    ],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an in-memory runner for the agent
runner = InMemoryRunner(agent=root_agent)


@app.post("/invoke")
async def invoke(request: Request):
    """
    Invokes the agent with a user query. Supports both legacy format and AI SDK format.

    Args:
        request: The request object, containing the user query in the body.

    Returns:
        The agent's response (JSON for legacy, streaming for AI SDK).
    """
    body = await request.json()

    # Check if this is an AI SDK request (has 'messages' field)
    if "messages" in body:
        # AI SDK format - extract latest user message
        messages = body.get("messages", [])
        user_message = ""
        for message in reversed(messages):
            if message.get("role") == "user":
                user_message = message.get("content", "")
                break

        # Get response from agent
        response = runner.run(user_input=user_message)

        # Stream the response in a format compatible with AI SDK
        def generate_stream():
            # Split response into chunks for streaming effect
            words = response.split()
            for i, word in enumerate(words):
                chunk_data = {
                    "choices": [
                        {
                            "delta": {
                                "content": word + (" " if i < len(words) - 1 else "")
                            }
                        }
                    ]
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"

            # End stream
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "http://localhost:5174",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
    else:
        # Legacy format - direct query
        query = body.get("query")
        response = runner.run(user_input=query)
        return Response(
            content=json.dumps({"response": response}),
            media_type="application/json",
            headers={
                "Access-Control-Allow-Origin": "http://localhost:5174",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )


@app.options("/invoke")
async def invoke_options():
    """Handle preflight CORS requests for /invoke endpoint."""
    return Response(
        content="",
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5174",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )


def create_frontend_router(build_dir="../frontend/dist"):
    """Creates a router to serve the React frontend.

    Args:
        build_dir: Path to the React build directory relative to this file.

    Returns:
        A Starlette application serving the frontend.
    """
    build_path = pathlib.Path(__file__).parent.parent.parent / build_dir

    if not build_path.is_dir() or not (build_path / "index.html").is_file():
        print(
            f"WARN: Frontend build directory not found or incomplete at {build_path}. Serving frontend will likely fail."
        )
        # Return a dummy router if build isn't ready
        from starlette.routing import Route

        async def dummy_frontend(request):
            return Response(
                "Frontend not built. Run 'npm run build' in the frontend directory.",
                media_type="text/plain",
                status_code=503,
            )

        return Route("/{path:path}", endpoint=dummy_frontend)

    return StaticFiles(directory=build_path, html=True)


# Mount the frontend under /app to not conflict with the LangGraph API routes
app.mount(
    "/app",
    create_frontend_router(),
    name="frontend",
)
