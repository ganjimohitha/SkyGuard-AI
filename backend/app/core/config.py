import os


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "SkyGuard AI")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./skyguard.db",
    )


settings = Settings()