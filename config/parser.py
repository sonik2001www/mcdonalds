import configparser
import os
from functools import lru_cache

from config.models import UrlConfig, Config, SettingsConfig, DatabaseConfig


@lru_cache
def load_config(path: str | None = None):
    if path is None:
        path = os.getenv("CONFIG_PATH", "secure.ini")

    parser = configparser.ConfigParser()
    parser.read(path)

    url = parser["url"]
    settings_data = parser["settings"]
    db_data = parser["database"]

    url_config = UrlConfig(
        url=url.get("url"),
        domain=url.get("domain"),
    )

    db_config = DatabaseConfig(
        user=db_data.get("db_user"),
        name=db_data.get("db_name"),
        host=db_data.get("db_host"),
        password=db_data.get("db_pass"),
    )

    settings_config = SettingsConfig(
        secret_key=settings_data.get("secret_key"),
        debug=settings_data.get("debug"),
    )

    return Config(
        url_config=url_config,
        settings_config=settings_config,
        db_config=db_config,
    )
