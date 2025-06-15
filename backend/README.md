# google-adk backend

this backend `requires-python = ">=3.11,<4.0"`

install and run the app using [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```

now you can run the app via the adk cli

```bash
adk web
```
