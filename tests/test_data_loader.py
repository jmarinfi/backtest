import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient

from app.data.data_loader import MarketDataLoader, KlineData
from app.models.market_data_models import KlineInterval


@pytest.fixture
def mock_client():
    """Mock AsyncClient para testing"""
    return AsyncMock(spec=AsyncClient)


@pytest.fixture  
def data_loader(mock_client):
    """MarketDataLoader con cliente mock"""
    return MarketDataLoader(mock_client)


@pytest.fixture
def sample_kline_response():
    """Respuesta de ejemplo de la API"""
    return [
        [
            1633024800000,  # open_time
            "50000.00",     # open
            "51000.00",     # high  
            "49500.00",     # low
            "50500.00",     # close
            "100.50",       # volume
            1633028399999,  # close_time
            "5075000.00",   # quote_asset_volume
            1500,           # number_of_trades
            "60.25",        # taker_buy_base_asset_volume
            "3045000.00",   # taker_buy_quote_asset_volume
            "0"             # ignore
        ]
    ]


@pytest.mark.asyncio
async def test_get_klines_success(data_loader, mock_client, sample_kline_response):
    """Test successful klines retrieval"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = sample_kline_response
    mock_client.get.return_value = mock_response
    
    # Call method
    result = await data_loader.get_klines(
        symbol="BTCUSDT",
        interval=KlineInterval.ONE_HOUR
    )
    
    # Verify API call
    mock_client.get.assert_called_once()
    call_args = mock_client.get.call_args
    assert "klines/extended" in call_args[0][0]
    assert call_args[1]["params"]["symbol"] == "BTCUSDT"
    assert call_args[1]["params"]["interval"] == "1h"
    
    # Verify response parsing
    assert len(result) == 1
    kline = result[0]
    assert isinstance(kline, KlineData)
    assert kline.open_time == 1633024800000
    assert kline.open == "50000.00"
    assert kline.close == "50500.00"


@pytest.mark.asyncio
async def test_get_klines_with_optional_params(data_loader, mock_client, sample_kline_response):
    """Test klines retrieval with optional parameters"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = sample_kline_response
    mock_client.get.return_value = mock_response
    
    # Call method with optional params
    await data_loader.get_klines(
        symbol="ETHUSDT",
        interval=KlineInterval.FIVE_MINUTES,
        start_time=1633024800000,
        end_time=1633028400000,
        limit=100
    )
    
    # Verify parameters were passed correctly
    call_args = mock_client.get.call_args
    params = call_args[1]["params"]
    assert params["symbol"] == "ETHUSDT"
    assert params["interval"] == "5m"
    assert params["startTime"] == 1633024800000
    assert params["endTime"] == 1633028400000
    assert params["limit"] == 100


@pytest.mark.asyncio
async def test_get_latest_klines(data_loader, mock_client, sample_kline_response):
    """Test helper method for getting latest klines"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = sample_kline_response
    mock_client.get.return_value = mock_response
    
    # Call helper method
    result = await data_loader.get_latest_klines(
        symbol="ADAUSDT",
        interval=KlineInterval.ONE_DAY,
        limit=50
    )
    
    # Verify correct parameters
    call_args = mock_client.get.call_args
    params = call_args[1]["params"]
    assert params["symbol"] == "ADAUSDT"
    assert params["interval"] == "1d"
    assert params["limit"] == 50
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_klines_api_error(data_loader, mock_client):
    """Test error handling when API call fails"""
    # Setup mock to raise exception
    mock_client.get.side_effect = Exception("API connection failed")
    
    # Verify exception is raised
    with pytest.raises(Exception) as exc_info:
        await data_loader.get_klines(
            symbol="BTCUSDT",
            interval=KlineInterval.ONE_HOUR
        )
    
    assert "API connection failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_klines_invalid_response_format(data_loader, mock_client):
    """Test handling of unexpected response format"""
    # Setup mock with invalid response format
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"invalid": "format"}  # Invalid format
    ]
    mock_client.get.return_value = mock_response
    
    # Call should succeed but return empty list
    result = await data_loader.get_klines(
        symbol="BTCUSDT",
        interval=KlineInterval.ONE_HOUR
    )
    
    assert len(result) == 0
