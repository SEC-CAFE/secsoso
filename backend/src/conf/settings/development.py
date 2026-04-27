import logging

from src.conf.settings.app import AppSettings


class DevAppSettings(AppSettings):
    title: str = "SECSOSO APIs DEV"
    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".envs/test.env"
