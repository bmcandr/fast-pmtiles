FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen --no-cache

COPY ./ .

CMD [".venv/bin/fastapi", "run", "src/fast_pmtiles/main.py", "--port", "80", "--host", "0.0.0.0"]