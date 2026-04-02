ruff format src
ruff check src
uv run pyright src
PYTHONPATH="src" uv run pytest -qr a src/test