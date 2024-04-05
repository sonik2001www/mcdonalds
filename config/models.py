from dataclasses import dataclass


@dataclass
class UrlConfig:
    url: str
    domain: str


@dataclass
class DatabaseConfig:
    user: str
    password: str
    host: str
    name: str


@dataclass
class SettingsConfig:
    secret_key: str
    debug: bool


@dataclass
class Config:
    url_config: UrlConfig
    settings_config: SettingsConfig
    db_config: DatabaseConfig
