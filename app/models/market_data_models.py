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
    ONE_MINUTE = "ONE_MINUTE"
    THREE_MINUTES = "THREE_MINUTES"
    FIVE_MINUTES = "FIVE_MINUTES"
    FIFTEEN_MINUTES = "FIFTEEN_MINUTES"
    THIRTY_MINUTES = "THIRTY_MINUTES"
    ONE_HOUR = "ONE_HOUR"
    TWO_HOURS = "TWO_HOURS"
    FOUR_HOURS = "FOUR_HOURS"
    SIX_HOURS = "SIX_HOURS"
    EIGHT_HOURS = "EIGHT_HOURS"
    TWELVE_HOURS = "TWELVE_HOURS"
    ONE_DAY = "ONE_DAY"
    THREE_DAYS = "THREE_DAYS"
    ONE_WEEK = "ONE_WEEK"
    ONE_MONTH = "ONE_MONTH"


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
