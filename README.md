# fast-pmtiles

A high-performance FastAPI-based vector tile server for [PMTiles](https://github.com/protomaps/PMTiles) archives.

[![codecov](https://codecov.io/gh/bmcandr/fast-pmtiles/graph/badge.svg?token=BQ8D0W3F54)](https://codecov.io/gh/bmcandr/fast-pmtiles)

## Features

- **Remote PMTiles Support**: Serve tiles directly from PMTiles archives hosted anywhere (S3, HTTP, etc.)
- **XYZ Tile API**: Standard `/tiles/{z}/{x}/{y}` endpoint compatible with any map client that supports MVT/PBF vector tiles
- **TileJSON Support**: Automatic TileJSON generation for easy client integration
- **Built-in Viewer**: Simple viewer included for instant visualization

## Installation

Requires Python 3.11 or higher.

* Install with [uv](https://github.com/astral-sh/uv):

  ```bash
  uv add fast-pmtiles
  ```

* Or `pip`:

   ```bash
   pip install fast-pmtiles
   ```

## Quick Start

1. **Run the server:**

   ```bash
   uvicorn fast_pmtiles.main:app
   ```

2. **View interactive Swagger docs:** <https://localhost:8000/docs>

3. **View tiles in your browser:**

   ```text
   http://localhost:8000/viewer?url=https://overturemaps-tiles-us-west-2-beta.s3.amazonaws.com/2026-01-21/places.pmtiles
   ```

4. **Get TileJSON description of the PMTiles source:**

  ```text
  http://localhost:8000/tilejson.json?url=https://overturemaps-tiles-us-west-2-beta.s3.amazonaws.com/2026-01-21/places.pmtiles
  ```

## Extending the application

```python
from fast_pmtiles import app

@app.get("/my-new-route")
def my_new_route():
   return {"status": "ok"}
```

## Configuration

See `.env.example`. Settings are defined in [settings.py](src/fast_pmtiles/settings.py).

## Development

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/bmcandr/fast-pmtiles.git
   cd fast-pmtiles
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

4. Run the server in development mode:

   ```bash
   fastapi dev src/fast_pmtiles/main.py
   ```

### Running Tests

```bash
uv run pytest
```

### Code Quality

This project uses:

- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [pre-commit](https://pre-commit.com/) for automated checks on commit

```bash
# Format code
ruff format

# Lint code
ruff check
```

## Acknowledgments

This project builds on the excellent work of:

- [PMTiles](https://github.com/protomaps/PMTiles) - Cloud-optimized archive format for pyramids of map tiles
- [async-pmtiles](https://github.com/developmentseed/async-pmtiles) - Async Python reader for PMTiles
- [obstore](https://github.com/developmentseed/obstore) - Highest-throughput Python interface to S3, GCS & Azure Storage
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [MapLibre GL JS](https://maplibre.org/) - Open-source map rendering library
