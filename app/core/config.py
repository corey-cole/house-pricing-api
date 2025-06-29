from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "House Pricing API"
    API_V1_STR: str = "/v1"

settings = Settings()