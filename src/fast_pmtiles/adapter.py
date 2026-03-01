from dataclasses import dataclass

from aiohttp import ClientSession
from async_pmtiles import Store

# source:
# https://github.com/developmentseed/async-pmtiles/blob/829fbe3c2b09c931afb77462133e70ecc68a3ba9/README.md


@dataclass
class AiohttpAdapter(Store):
    session: ClientSession

    async def get_range_async(
        self,
        path: str,
        *,
        start: int,
        length: int,
    ) -> bytes:
        inclusive_end = start + length - 1
        headers: dict[str, str] = {"Range": f"bytes={start}-{inclusive_end}"}
        async with self.session.get(path, headers=headers) as response:
            return await response.read()
