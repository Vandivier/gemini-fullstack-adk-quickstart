# gemini-fullstack-adk-quickstart

Get started with building Fullstack Agents using google-adk

## usage

1. populate `GEMINI_API_KEY` in `backend/.env`
2. install the backend and front end
3. activate the backend uv venv, as mentioned in backend/README.md
4. from this root dir, with the uv venv active, `make dev`
5. visit the UI at the location given in the CLI as a result of (2)

a prompt I like to use to prove the model is connecting to the web is `what day of the week is today?`

## background and motivation

this project was inspired by [gemini-fullstack-langgraph-quickstart](https://github.com/google-gemini/gemini-fullstack-langgraph-quickstart)

I thought "Why would I prefer LangGraph over Google's own google-adk?"

I wasn't sure, so I built this POC to compare the implementations.

Other interesting Google Quickstarts:

- <https://github.com/google-gemini/gemini-api-quickstart>
- <https://github.com/google-gemini/gemini-image-editing-nextjs-quickstart>

It's also interesting to compare a more fully-featured agentic app:
[gng-ai](https://github.com/Vandivier/gng-ai): google-centric dnd with agents
