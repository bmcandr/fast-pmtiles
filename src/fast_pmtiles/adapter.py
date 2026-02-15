from dataclasses import dataclass

from aiohttp import ClientSession
from async_pmtiles import Store


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
        headers = {"Range": f"bytes={start}-{inclusive_end}"}
        async with self.session.get(path, headers=headers) as response:
            return await response.read()
