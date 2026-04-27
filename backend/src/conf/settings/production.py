from src.conf.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    title: str = "SECSOSO APIs"

    class Config(AppSettings.Config):
        env_file = ".envs/prod.env"
