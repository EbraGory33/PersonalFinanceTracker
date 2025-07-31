import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


class Settings(BaseSettings):
    
    MODE: str = os.getenv("MODE", "development")

    # Dynamic cookie settings
    @property
    def SECURE_COOKIE(self) -> bool:
        return self.MODE == "production"

    @property
    def SAME_SITE(self) -> str:
        # Use None for cross-site in production (requires Secure=True)
        return "none" if self.MODE == "production" else "lax"
    
    Frontend_Url: str
    
    ACCESS_TOKEN_SECRET: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # Plaid
    PLAID_CLIENT_ID: str
    PLAID_SECRET: str
    PLAID_ENV: str = "sandbox"
    PLAID_PRODUCT: List[str]
    PLAID_COUNTRY_CODE: List[str]

    #DWOLLA
    DWOLLA_ENV: str = "sandbox"
    DWOLLA_KEY: str
    DWOLLA_SECRET: str
    DWOLLA_BASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    @property
    def postgres_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]  # default

    class Config:
        # Read environment variables from .env file
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        json_encoders = {
            list: lambda v: ",".join(v)  # so you can pass BACKEND_CORS_ORIGINS as comma-separated env var
        }

# Initialize settings
settings = Settings()
