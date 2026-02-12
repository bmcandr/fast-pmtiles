import asyncio
from pathlib import Path
from urllib.parse import quote, unquote

from aiohttp import ClientSession
from async_pmtiles import PMTilesReader
from cachetools import LRUCache
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from starlette.templating import Jinja2Templates

from fast_pmtiles.adapter import AiohttpAdapter
from fast_pmtiles.middleware import CacheControlMiddleware, RequestTimingMiddleware
from fast_pmtiles.settings import APISettings

settings = APISettings()

jinja2_env = Environment(
    loader=FileSystemLoader(f"{Path(__file__).resolve().parent}/templates")
)
templates = Jinja2Templates(env=jinja2_env)


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = ClientSession()
    app.state.store = AiohttpAdapter(session=session)
    # cache PMTilesReaders per source URI
    app.state.get_reader_task_cache: LRUCache = LRUCache(maxsize=32)
    yield
    await session.close()


app = FastAPI(
    title=settings.title,
    description="Vector tile server for PMTiles sources.",
    lifespan=lifespan,
    root_path=settings.root_path,
)

app.add_middleware(RequestTimingMiddleware)  # type: ignore
app.add_middleware(
    CacheControlMiddleware,  # type: ignore
    cache_control_str=settings.cache_control_str,
)


async def get_reader(url: str, request: Request) -> PMTilesReader:
    """Return cached PMTilesReader instance if available, otherwise create."""
    task_cache = request.app.state.get_reader_task_cache
    if task := task_cache.get(url):
        return await task

    async def open_reader():
        return await PMTilesReader.open(
            unquote(url),
            store=request.app.state.store,
        )

    # cache future
    task = asyncio.create_task(open_reader())
    task_cache[url] = task

    try:
        return await task
    except Exception:
        # invalidate
        task_cache.pop(url, None)
        raise


async def _get_tilejson(
    url: str,
    request: Request,
    reader: PMTilesReader = Depends(get_reader),
):
    tiles_url = (
        request.url_for(
            "get_tile",
            z="{z}",
            x="{x}",
            y="{y}",
        )._url
        + f"?url={quote(url)}"
    )
    return {
        "tilejson": "3.0.0",
        "scheme": "xyz",
        "tiles": [tiles_url],
        "bounds": reader.bounds,
        "center": reader.center,
        "minzoom": reader.minzoom,
        "maxzoom": reader.maxzoom,
        **await reader.metadata(),
    }


@app.get(
    "/tilejson.json",
    operation_id="getTilejson",
)
async def get_tilejson(
    url: str,
    request: Request,
    reader: PMTilesReader = Depends(get_reader),
):
    """Get TileJSON description of PMTiles archive."""
    return await _get_tilejson(url, request, reader)


class TileResponse(Response):
    media_type = "application/vnd.mapbox-vector-tile"


@app.get(
    "/tiles/{z}/{x}/{y}",
    status_code=status.HTTP_200_OK,
    response_class=TileResponse,
    operation_id="getTile",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Tile not found"},
    },
)
async def get_tile(
    z: int,
    x: int,
    y: int,
    reader: PMTilesReader = Depends(get_reader),
):
    """Get tile."""
    tile = await reader.get_tile(x=x, y=y, z=z)
    return TileResponse(
        tile,
        headers={"Content-Encoding": "gzip"},
    )


@app.get("/viewer")
async def viewer(
    url: str,
    request: Request,
    reader: PMTilesReader = Depends(
        get_reader,
    ),
):
    tilejson = await _get_tilejson(url, request, reader)

    # todo: layer selection?
    layer = tilejson["vector_layers"][0]

    return HTMLResponse(
        templates.get_template("viewer.html").render(
            center=list(tilejson["center"][:2]),
            zoom=layer["minzoom"],
            id=layer["id"],
            tiles=tilejson["tiles"],
            minzoom=layer["minzoom"],
            maxzoom=layer["maxzoom"],
            attribution=tilejson["attribution"],
        )
    )


@app.get(
    "/healthz",
    tags=["health"],
    operation_id="healthCheck",
)
def health():
    """Health check."""
    return {"status": "ok"}
