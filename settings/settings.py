from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    environment: str = Field("dev", env="ENVIRONMENT")
    app_name: str = Field("dentalstall.com scraper", env="APP_NAME")
    images_folder: str = Field("assets")
    max_page_limit: int = Field(10, env="MAX_PAGE_LIMIT")
    auth_token: str = Field(..., env="AUTH_TOKEN")
    proxy: Optional[str] = Field(None, env="PROXY")

    # redis
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")

    # logger settings
    log_file: str = Field("logs/app.log", env="LOG_FILE")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # dentalstall.com
    dentalstall_base_url: str = Field(
        "https://dentalstall.com/shop", env="DENTALSTALL_BASE_URL"
    )
    dentalstall_max_retries: int = Field(5)
    output_json_filename: str = Field("outputs.json")

    class Config:
        env_file = ".env.dev"


class ProductionSettings(Settings):
    class Config:
        env_file = ".env.prod"


def fetch_settings():
    settings = Settings()
    if settings.environment == "production":
        settings = ProdSettings()
    return settings
