#!/usr/bin/env python
# encoding: utf-8

import sentry_sdk
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.handler.exception.http_error import http_error_handler
from src.handler.exception.validation_error import http422_error_handler
from src.routers.api import router as api_router
from src.conf.config import get_app_settings


def get_application() -> FastAPI:
    settings = get_app_settings()
    if not settings.debug:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production,
            traces_sample_rate=1.0,
        )

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = get_application()
