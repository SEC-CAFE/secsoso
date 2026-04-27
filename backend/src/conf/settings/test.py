import logging

from src.conf.settings.app import AppSettings


class TestAppSettings(AppSettings):
    title: str = "SECSOSO TEST"
    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".envs/test.env"
