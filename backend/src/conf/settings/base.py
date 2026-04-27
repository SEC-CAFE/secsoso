from enum import Enum

from pydantic import BaseSettings


class AppEnvTypes(str, Enum):
    prod: str = "prod"  # type: ignore
    dev: str = "dev"  # type: ignore
    test: str = "test"  # type: ignore


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod  # type: ignore

    class Config:
        env_file = ".envs/.env"
