
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="allow")

    SIM_MODE: bool = True
    AUTO_TRADE: bool = True
    SYMBOLS: str = "KRX:005930,US:AAPL"

    DB_URL: str = "sqlite:///./data/app.db"

    INIT_CASH_KRW: float = 10000000.0
    INIT_CASH_USD: float = 5000.0
    FX_USDKRW: float = 1350.0

    COOLDOWN_BARS: int = 10
    CONFIRM_BARS: int = 2
    HYSTERESIS_PCT: float = 0.003
    DAILY_TRADE_LIMIT: int = 8
    NO_PYRAMIDING: bool = True

    KIS_BASE: str = "https://openapivts.koreainvestment.com:29443"
    KIS_APP_KEY: Optional[str] = None
    KIS_APP_SECRET: Optional[str] = None
    KIS_CANO: Optional[str] = None
    KIS_ACNT_PRDT_CD: str = "01"

    KIS_TR_DOM_BAL_PATH: Optional[str] = None
    KIS_TR_DOM_BAL_ID: Optional[str] = None
    KIS_TR_DOM_DEPOSIT_PATH: Optional[str] = None
    KIS_TR_DOM_DEPOSIT_ID: Optional[str] = None
    KIS_TR_OS_BAL_PATH: Optional[str] = None
    KIS_TR_OS_BAL_ID: Optional[str] = None

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

settings = Settings()
