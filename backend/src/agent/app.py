# mypy: disable - error - code = "no-untyped-def,misc"
import pathlib
from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from google.adk.runners import InMemoryRunner
from agent.agent import root_agent

# Define the FastAPI app
app = FastAPI()

# Create an in-memory runner for the agent
runner = InMemoryRunner(agent=root_agent)


@app.post("/invoke")
async def invoke(request: Request):
    """Invokes the agent with a user query.

    Args:
        request: The request object, containing the user query in the body.

    Returns:
        The agent's response to the query.
    """
    # get the user query from the request body
    body = await request.json()
    query = body.get("query")

    # invoke the agent with the user query
    response = runner.run(user_input=query)

    return {"response": response}


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
