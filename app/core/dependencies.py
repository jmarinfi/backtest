from typing import Any, AsyncGenerator

from httpx import AsyncClient, Limits


async def get_http_client() -> AsyncGenerator[AsyncClient, Any]:
    limits = Limits(max_keepalive_connections=5, max_connections=10)
    async with AsyncClient(limits=limits, timeout=30.0) as client:
        yield client
