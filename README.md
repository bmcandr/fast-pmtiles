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

* Clone the repo
* Install with [uv](https://github.com/astral-sh/uv):

  ```bash
  uv sync
  ```

## Quick Start

1. **Run the server:**

   ```bash
   uv run fastapi dev fast_pmtiles/main.py
   ```

1. **View tiles in your browser:**

   ```text
   http://localhost:8000/viewer?url=https://overturemaps-tiles-us-west-2-beta.s3.amazonaws.com/2026-01-21/places.pmtiles
   ```

2. **Get TileJSON description of the PMTiles source:**

  ```text
  http://localhost:8000/tilejson.json?url=https://overturemaps-tiles-us-west-2-beta.s3.amazonaws.com/2026-01-21/places.pmtiles
  ```

## API Endpoints

### Get TileJSON

```http
GET /tilejson.json?url={pmtiles_url}
```

Returns a [TileJSON](https://github.com/mapbox/tilejson-spec) description of the PMTiles archive.

**Parameters:**

- `url`: URL-encoded absolute URL of the PMTiles archive

### Get Tile

```http
GET /tiles/{z}/{x}/{y}?url={pmtiles_url}
```

Returns a vector tile in Mapbox Vector Tile (MVT) format.

**Parameters:**

- `z`, `x`, `y`: Tile coordinates (zoom, x, y)
- `url`: URL-encoded absolute URL of the PMTiles archive

### Viewer

```http
GET /viewer?url={pmtiles_url}
```

Returns an interactive HTML map viewer for visualizing the tiles.

### Health Check

```http
GET /healthz
```

Returns server health status.

## Configuration

Configure the server using environment variables or a `.env` file:

```bash
# Optional: Custom server title
FAST_PMTILES_TITLE="My PMTiles Server"

# Optional: CORS origins (default: "*")
FAST_PMTILES_CORS_ORIGINS="*"

# Optional: Cache-Control header (default: "public, max-age=3600")
FAST_PMTILES_CACHE_CONTROL_STR="public, max-age=86400"

# Optional: Root path for proxy deployments (default: "")
FAST_PMTILES_ROOT_PATH="/"
```

## Development

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fast-pmtiles.git
   cd fast-pmtiles
   ```

1. Install dependencies:

   ```bash
   uv sync
   ```

1. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

### Running Tests

```bash
uv run pytest
```

### Code Quality

This project uses:

- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [pre-commit](https://pre-commit.com/) for automated checks

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
- [obstore](https://github.com/developmentseed/obstore)
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [MapLibre GL JS](https://maplibre.org/) - Open-source map rendering library
