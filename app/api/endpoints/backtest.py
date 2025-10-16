import logging
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient

from app.core.config import settings
from app.core.dependencies import get_http_client
from app.models.market_data_models import ExchangeInfo


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
