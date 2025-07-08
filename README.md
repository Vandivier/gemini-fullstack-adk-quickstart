# gemini-fullstack-adk-quickstart

Get started with building Fullstack Agents using google-adk

## usage

1. populate `GEMINI_API_KEY` in `backend/.env`
2. install the backend and front end
3. activate the backend uv venv, as mentioned in backend/README.md
4. from this root dir, with the uv venv active, `make dev`
5. verify servers are running on ports 5173 (frontend) and 8000 (backend)
    a. if this is not the case, consider running `make cleanup`
6. visit the UI at the location given in the CLI as a result of (2)

a prompt I like to use to prove the model is connecting to the web is `what day of the week is today?`

## production

This app can be a useful starting point for a production agent, but it's not intended to ship directly to production.

Most notably, make file commands all assume a development build and they rely on using dev server forms of the frontend and backend. If you want to deploy to production, use the Dockerfile and make sure a fresh frontend build is included for every production deployment, using `npm run build` rather than running the vite dev server in production.

The FastAPI server will run your static build on port 8000, avoiding CORS issues.

## background and motivation

this project was inspired by [gemini-fullstack-langgraph-quickstart](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart)

I thought "Why would I prefer LangGraph over Google's own google-adk?"

I wasn't sure, so I built this POC to compare the implementations.

Other interesting Google Quickstarts:

- <https://github.com/google-gemini/gemini-api-quickstart>
- <https://github.com/google-gemini/gemini-image-editing-nextjs-quickstart>

It's also interesting to compare a more fully-featured agentic app:
[gng-ai](https://github.com/Vandivier/gng-ai): google-centric dnd with agents

Notably, this repo uses the Vercel AI SDK on the front end.

[This article](https://medium.com/@jjaladi/langgraph-vs-adk-a-developers-guide-to-choosing-the-right-ai-agent-framework-b59f756bcd98) also provides an interesting comparison for choosing google-adk or langgraph.
