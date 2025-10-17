import logging
from typing import Any, Optional, Union
from httpx import AsyncClient
from pydantic import BaseModel

from app.core.config import settings
from app.models.market_data_models import KlineInterval


logger = logging.getLogger(__name__)


class Candlestick(BaseModel):
    openTime: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    closeTime: int
    quoteAssetVolume: str
    numberOfTrades: int
    takerBuyBaseAssetVolume: str
    takerBuyQuoteAssetVolume: str
    ignore: str


class MarketDataLoader:
    """Cliente para comunicarse con el microservicio connect y descargar datos de mercado"""
    
    def __init__(self, client: AsyncClient):
        self.client = client
        self.base_url = f"{settings.base_url_api_connect}/klines/extended"
    
    async def get_klines(
        self,
        symbol: str,
        interval: KlineInterval,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = 2000
    ) -> list[Candlestick]:
        """
        Descarga datos de klines del microservicio connect
        """
        params: dict[str, Union[str, int]] = {
            "symbol": symbol,
            "interval": interval.value
        }
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if limit is not None:
            params["limit"] = limit
            
        logger.info(f"Requesting klines for {symbol} with params: {params}")
        try:
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Received {len(data)} klines for {symbol}")
            
            # data es una lista de dicts con claves exactas como en connect
            klines: list[Candlestick] = []
            for item in data:
                if isinstance(item, dict):
                    klines.append(Candlestick(**item))
                else:
                    logger.warning(f"Unexpected kline item type: {type(item)}")
            return klines
        except Exception as e:
            logger.error(f"Error fetching klines for {symbol}: {e}")
            raise
    
    async def get_latest_klines(
        self,
        symbol: str,
        interval: KlineInterval,
        limit: int = 100
    ) -> list[Candlestick]:
        return await self.get_klines(symbol=symbol, interval=interval, limit=limit)
