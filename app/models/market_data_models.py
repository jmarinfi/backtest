from enum import Enum
from pydantic import BaseModel


class RateLimitType(str, Enum):
    REQUEST_WEIGHT = "REQUEST_WEIGHT"
    ORDERS = "ORDERS"
    RAW_REQUESTS = "RAW_REQUESTS"


class RateLimitInterval(str, Enum):
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    DAY = "DAY"


class KlineInterval(str, Enum):
    ONE_MINUTE = "1m"
    THREE_MINUTES = "3m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    TWO_HOURS = "2h"
    FOUR_HOURS = "4h"
    SIX_HOURS = "6h"
    EIGHT_HOURS = "8h"
    TWELVE_HOURS = "12h"
    ONE_DAY = "1d"
    THREE_DAYS = "3d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1M"


class RateLimit(BaseModel):
    rateLimitType: RateLimitType
    interval: RateLimitInterval
    intervalNum: int
    limit: int


class SymbolInfo(BaseModel):
    symbol: str
    status: str
    baseAsset: str
    baseAssetPrecision: int
    quoteAsset: str
    quoteAssetPrecision: int
    baseCommissionPrecision: int
    quoteCommissionPrecision: int
    orderTypes: list[str]
    icebergAllowed: bool
    ocoAllowed: bool
    otoAllowed: bool
    quoteOrderQtyMarketAllowed: bool
    allowTrailingStop: bool
    cancelReplaceAllowed: bool
    amendAllowed: bool
    pegInstructionsAllowed: bool
    isSpotTradingAllowed: bool
    isMarginTradingAllowed: bool
    filters: list[dict[str, object]]
    permissions: list[str]
    permissionSets: list[list[str]]
    defaultSelfTradePreventionMode: str
    allowedSelfTradePreventionModes: list[str]


class ExchangeInfo(BaseModel):
    timezone: str
    serverTime: int
    rateLimits: list[RateLimit]
    exchangeFilters: list[dict[str, str]]
    symbols: list[SymbolInfo]


class Candlestick(BaseModel):
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
