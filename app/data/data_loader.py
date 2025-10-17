from io import StringIO
import logging
from typing import Any, Optional, Union
from httpx import AsyncClient
from pydantic import BaseModel
import pandas as pd

from app.core.config import settings
from app.models.market_data_models import Candlestick, KlineInterval


logger = logging.getLogger(__name__)


class MarketDataLoader:
    """Cliente para comunicarse con el microservicio connect y descargar datos de mercado"""
    
    def __init__(self, client: AsyncClient):
        self.client = client
        self.base_url_klines = f"{settings.base_url_api_connect}/klines"
        self.base_url_klines_extended = f"{settings.base_url_api_connect}/klines/extended"
    
    async def get_klines(
        self,
        symbol: str,
        interval: KlineInterval,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = 500
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
            response = await self.client.get(self.base_url_klines, params=params)
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
    

    async def get_klines_extended_csv(
        self,
        symbol: str,
        interval: KlineInterval,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = 2000
    ) -> str:
        """
        Descarga datos en CSV de klines del microservicio connect superando los límites estándar del exchange con paginación
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
            response = await self.client.get(self.base_url_klines_extended, params=params)
            response.raise_for_status()

            # Obtener el CSV como texto
            csv_content = response.text
            total_klines = response.headers.get("X-Total-Klines", "0")
            logger.info(f"Received CSV with {total_klines} klines for {symbol}")

            return csv_content

        except Exception as e:
            logger.error(f"Error fetching klines for {symbol}: {e}")
            raise

    async def get_klines_extended_df(
        self,
        symbol: str,
        interval: KlineInterval,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        limit: Optional[int] = 2000
    ) -> pd.DataFrame:
        """
        Versión que retorna DataFrame directamente (más eficiente para backtesting)
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
            response = await self.client.get(self.base_url_klines_extended, params=params)
            response.raise_for_status()

            csv_content = response.text
            df = pd.read_csv(StringIO(csv_content))

            df['openTime'] = pd.to_datetime(df['openTime'], unit='ms')
            df['closeTime'] = pd.to_datetime(df['closeTime'], unit='ms')
            df[['open', 'high', 'low', 'close', 'volume', 'quoteAssetVolume',
                'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume']] = df[[
                'open', 'high', 'low', 'close', 'volume', 'quoteAssetVolume',
                'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume']].astype(float)
            df['numberOfTrades'] = df['numberOfTrades'].astype(int)

            return df

        except Exception as e:
            logger.error(f"Error fetching klines for {symbol}: {e}")
            raise
