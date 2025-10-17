import logging
from typing import Optional, Any
from httpx import AsyncClient
from pydantic import BaseModel

from app.core.config import settings
from app.models.market_data_models import KlineInterval


logger = logging.getLogger(__name__)


class KlineData(BaseModel):
    """Modelo simple para datos de kline"""
    open_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    close_time: int
    quote_asset_volume: str
    number_of_trades: int
    taker_buy_base_asset_volume: str
    taker_buy_quote_asset_volume: str
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
        limit: Optional[int] = None
    ) -> list[KlineData]:
        """
        Descarga datos de klines del microservicio connect
        
        Args:
            symbol: Símbolo del par de trading (ej: "BTCUSDT")
            interval: Intervalo temporal de las klines
            start_time: Timestamp de inicio (opcional)
            end_time: Timestamp de fin (opcional) 
            limit: Número máximo de klines a retornar (opcional)
            
        Returns:
            Lista de datos de klines
            
        Raises:
            Exception: Si hay error en la comunicación con el microservicio
        """
        params = {
            "symbol": symbol,
            "interval": interval.value
        }
        
        # Agregar parámetros opcionales si se proporcionan
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
            
            # Convertir la respuesta a objetos KlineData
            klines = []
            for kline_raw in data:
                # Asumiendo que la API retorna arrays de valores por kline
                if isinstance(kline_raw, list) and len(kline_raw) >= 12:
                    kline = KlineData(
                        open_time=kline_raw[0],
                        open=str(kline_raw[1]),
                        high=str(kline_raw[2]),
                        low=str(kline_raw[3]),
                        close=str(kline_raw[4]),
                        volume=str(kline_raw[5]),
                        close_time=kline_raw[6],
                        quote_asset_volume=str(kline_raw[7]),
                        number_of_trades=kline_raw[8],
                        taker_buy_base_asset_volume=str(kline_raw[9]),
                        taker_buy_quote_asset_volume=str(kline_raw[10]),
                        ignore=str(kline_raw[11])
                    )
                    klines.append(kline)
                else:
                    logger.warning(f"Unexpected kline format: {kline_raw}")
                    
            return klines
            
        except Exception as e:
            logger.error(f"Error fetching klines for {symbol}: {e}")
            raise
    
    async def get_latest_klines(
        self,
        symbol: str,
        interval: KlineInterval,
        limit: int = 100
    ) -> list[KlineData]:
        """
        Método helper para obtener las klines más recientes
        
        Args:
            symbol: Símbolo del par de trading
            interval: Intervalo temporal
            limit: Número de klines a retornar (default: 100)
            
        Returns:
            Lista de klines más recientes
        """
        return await self.get_klines(symbol=symbol, interval=interval, limit=limit)
    
    async def get_historical_klines(
        self,
        symbol: str,
        interval: KlineInterval,
        start_time: int,
        end_time: Optional[int] = None
    ) -> list[KlineData]:
        """
        Método helper para obtener datos históricos en un rango de tiempo
        
        Args:
            symbol: Símbolo del par de trading
            interval: Intervalo temporal
            start_time: Timestamp de inicio
            end_time: Timestamp de fin (opcional)
            
        Returns:
            Lista de klines históricas
        """
        return await self.get_klines(
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time
        )
