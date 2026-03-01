FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

COPY . /app

# Disable development dependencies
ENV UV_NO_DEV=1

WORKDIR /app

RUN uv sync --frozen --no-cache

ENV PATH="/app/.venv/bin:$PATH"

CMD ["fastapi", "run", "src/fast_pmtiles/main.py", "--port", "80", "--host", "0.0.0.0"]