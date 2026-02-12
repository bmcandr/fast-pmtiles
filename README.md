# fast-pmtiles

A simple OGC Tiles API for PMTiles.

Built with:

* [FastAPI](https://github.com/fastapi/fastapi)
* [async-pmtiles](https://github.com/developmentseed/async-pmtiles)
* [obstore](https://github.com/developmentseed/obstore)

_Work in progress..._

## Quickstart

* `uv sync`
* `uv run fastapi dev fast_pmtiles/main.py`
* Docs @ http://localhost:8000/docs
* Viewer example with Overture Places: http://localhost:8000/viewer?url=https%253A%2F%2Foverturemaps-tiles-us-west-2-beta.s3.amazonaws.com%2F2026-01-21%2Fplaces.pmtiles

_Note: URLs passed as query parameters must be URL encoded._
