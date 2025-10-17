from typing import Any, AsyncGenerator

from httpx import AsyncClient, Limits

from app.data.data_loader import MarketDataLoader


async def get_http_client() -> AsyncGenerator[AsyncClient, Any]:
    limits = Limits(max_keepalive_connections=5, max_connections=10)
    async with AsyncClient(limits=limits, timeout=30.0) as client:
        yield client


async def get_market_data_loader() -> AsyncGenerator[MarketDataLoader, Any]:
    """Dependencia para obtener el MarketDataLoader con cliente HTTP configurado"""
    limits = Limits(max_keepalive_connections=5, max_connections=10)
    async with AsyncClient(limits=limits, timeout=30.0) as client:
        loader = MarketDataLoader(client)
        yield loader
