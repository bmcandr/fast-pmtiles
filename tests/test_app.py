from unittest.mock import AsyncMock
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from fast_pmtiles import app
from fast_pmtiles.main import get_reader

OVERTURE_RELEASE = "2026-01-21"
OVERTURE_BUCKET = "overturemaps-tiles-us-west-2-beta"


@pytest.fixture
def http_url() -> str:
    return quote(
        f"https://{OVERTURE_BUCKET}.s3.amazonaws.com/{OVERTURE_RELEASE}/places.pmtiles"
    )


@pytest.fixture
def s3_url() -> str:
    return quote(f"s3://{OVERTURE_BUCKET}/{OVERTURE_RELEASE}/places.pmtiles")


@pytest.mark.vcr()
@pytest.mark.parametrize("url", ["http_url", "s3_url"])
def test_get_tilejson(url, request):
    with TestClient(app) as client:
        r = client.get(f"/tilejson.json?url={request.getfixturevalue(url)}")
        assert r.status_code == 200
        tilejson = r.json()

        assert tilejson.get("tiles")


@pytest.mark.vcr()
def test_viewer(http_url):
    with TestClient(app) as client:
        r = client.get(f"/viewer?url={http_url}")
        assert r.status_code == 200


@pytest.mark.vcr()
def test_get_tile(http_url):
    with TestClient(app) as client:
        r = client.get(f"/tiles/0/0/0?url={http_url}")
        assert r.status_code == 200


def test_get_tile_404():
    def get_mock_reader():
        mock_reader = AsyncMock()
        mock_reader.get_tile.return_value = None
        return mock_reader

    with TestClient(app) as client:
        app.dependency_overrides[get_reader] = get_mock_reader
        r = client.get(f"/tiles/0/0/0?url={http_url}")
        assert r.status_code == 404
        app.dependency_overrides.clear()


def test_get_reader_cache(http_url):
    with TestClient(app) as client:
        route = f"/tilejson.json?url={http_url}"
        for _ in range(2):
            r = client.get(route)
            assert r.status_code == 200


def test_healthcheck():
    with TestClient(app) as client:
        r = client.get("/healthz")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
