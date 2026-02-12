from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    title: str = "fast-pmtiles: OGC Tiles API from PMTiles Sources"
    cors_origins: str = "*"
    cache_control_str: str = "public, max-age=3600"
    root_path: str = ""

    model_config = SettingsConfigDict(
        env_prefix="FAST_PMTILES_",
        env_file=".env",
        extra="ignore",
    )
