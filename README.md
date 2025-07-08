# gemini-fullstack-adk-quickstart

Get started with building Fullstack Agents using google-adk

## Usage

1. populate `GEMINI_API_KEY` in `backend/.env`
2. install the backend and front end
3. activate the backend uv venv, as mentioned in backend/README.md
4. from this root dir, with the uv venv active, `make dev`
5. verify servers are running on ports 5173 (frontend) and 8000 (backend)
    a. if this is not the case, consider running `make cleanup`
6. visit the UI at the location given in the CLI as a result of (2)

a prompt I like to use to prove the model is connecting to the web is `what day of the week is today?`

### Run the Agent in Isolation

After you complete the usage instructions, you can simply run `adk web` in the backend/ directory. Assuming you have already sourced your virtual environment,you should be able to interact with the agent in isolation on the ADK Playground at:
<http://localhost:8000/dev-ui/?app=src>

This is also useful as a troubleshooting tip, to avoid issues related to Vite, FastAPI, Docker, uvicorn, and so on.

### Copilot Instructions

This app is equipped with backend/scripts/copilot-instructions.txt which can greatly improve AI assistant performance when loaded in context.

Refresh the instructions with `make instructions`.

Try using a few different models and using the web search tool.

## Production

Makefile commands assume a developer environment. The Dockerfile is encouraged for production work. Notably, it forces a static build of the frontend which is then served through the same uvicorn port (8000 by default), avoiding CORS issues.

```bash
docker build -t adk-quickstart .
docker run -p 8000:8000 adk-quickstart
```

Then, visit `http://localhost:8000/app/` or your analogously configured UI URL.

## Contributing

Bug fixes, documentation improvements, and version bumps are all welcome!

This is intended to be a basic agent boilerplate. As such, please make feature requests elsewhere. Three better-fit locations for those requests include:

1. [basic-gemini-chat](https://github.com/Vandivier/basic-gemini-chat), a collection of various gemini apps and architectures
2. [genai-oneshots](https://github.com/Vandivier/genai-oneshots), a collection for all kinds of Generative AI applications, including WIP and vibe coded projects
3. Chat about making a totally new app with the [Ladderly.io](https://www.ladderly.io/) community on [Discord](https://discord.com/invite/fAg6Xa4uxc)

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

Learn more about building agents with the [Google ADK here](https://google.github.io/adk-docs/agents/)!

## troubleshooting

1. Read this README in full, notably the bit on Copilot Instructions
2. try running the app three different ways to help pinpoint your issue:
    1. `make dev`
    2. `make debug-dev`
    3. through Docker
3. if you `npm run build` the ui and run that static build locally, be sure to clear your cache and rebuild when you make changes.
