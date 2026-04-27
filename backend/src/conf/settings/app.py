import logging
import sys
from typing import Any, Dict, List, Tuple

from loguru import logger

from src.utils.logging import InterceptHandler
from src.conf.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = ""
    openapi_prefix: str = ""
    openapi_url: str = ""
    redoc_url: str = ""
    title: str = "SECSOSO"
    version: str = "1.0"
    site_url: str = ""

    sentry_dsn: str = ""
    sear_xng_url: str = ""
    sear_xng_safe: int = 0
    contexts_limit: int = 8

    ollama_url: str = ""
    proxy_auth: str = ""
    llm_provider: str = "moonshot"
    llm_model: str = "moonshot-v1-8k"
    llm_base_url: str = ""
    llm_api_key: str = ""

    api_prefix: str = ""
    # api_prefix: str = "/api"
    jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
