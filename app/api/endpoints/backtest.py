import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from httpx import AsyncClient

from app.core.config import settings
from app.core.dependencies import get_http_client, get_market_data_loader
from app.models.market_data_models import Candlestick, ExchangeInfo, KlineInterval
from app.data.data_loader import MarketDataLoader


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/exchange-info")
async def get_exchange_info(client: AsyncClient = Depends(get_http_client)) -> ExchangeInfo:
    try:
        response = await client.get(f"{settings.base_url_api_connect}/exchange-info")
        response.raise_for_status()
        data = response.json()

        logger.info("Fetched exchange info data: %s", data)
        return ExchangeInfo(**data)

    except HTTPException:
        raise

    except Exception as e:
        logger.error("Error fetching exchange info: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/klines")
async def get_klines(
    symbol: str = Query(..., description="Trading pair symbol (e.g., BTCUSDT)"),
    interval: KlineInterval = Query(..., description="Kline interval"),
    start_time: Optional[int] = Query(None, description="Start time as timestamp"),
    end_time: Optional[int] = Query(None, description="End time as timestamp"), 
    limit: Optional[int] = Query(None, description="Number of klines to return"),
    loader: MarketDataLoader = Depends(get_market_data_loader)
) -> list[Candlestick]:
    """
    Obtiene datos de klines del microservicio connect
    """
    try:
        klines = await loader.get_klines(
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit
        )
        
        logger.info(f"Retrieved {len(klines)} klines for {symbol}")
        return klines
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error fetching klines for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/klines/latest")
async def get_latest_klines(
    symbol: str = Query(..., description="Trading pair symbol (e.g., BTCUSDT)"),
    interval: KlineInterval = Query(..., description="Kline interval"),
    limit: int = Query(100, description="Number of latest klines to return"),
    loader: MarketDataLoader = Depends(get_market_data_loader)
) -> list[Candlestick]:
    """
    Obtiene las klines más recientes para un símbolo
    """
    try:
        klines = await loader.get_latest_klines(
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        
        logger.info(f"Retrieved {len(klines)} latest klines for {symbol}")
        return klines
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error fetching latest klines for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/klines/extended")
async def get_extended_klines_csv(
    symbol: str = Query(..., description="Trading pair symbol (e.g., BTCUSDT)"),
    interval: KlineInterval = Query(..., description="Kline interval"),
    start_time: Optional[int] = Query(None, description="Start time as timestamp"),
    end_time: Optional[int] = Query(None, description="End time as timestamp"), 
    limit: Optional[int] = Query(2000, description="Number of klines to return"),
    loader: MarketDataLoader = Depends(get_market_data_loader)
) -> Response:
    """
    Obtiene datos de klines en formato CSV superando los límites estándar del exchange
    """
    try:
        klines_csv = await loader.get_klines_extended_csv(
            symbol=symbol,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            limit=limit
        )
        return Response(
            content=klines_csv,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{symbol}_{interval.value}.csv"'},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching extended klines for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
