import json
import logging
import os
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Mapping

SECRETS_PATH = Path(__file__).resolve().parents[2] / "wainlog-secrets.json"


@dataclass
class ConfigValues:
    "Non-secret config values"
    GOOGLE_OAUTH_AUTHORIZE_URL: str
    GOOGLE_OAUTH_TOKEN_URL: str
    GOOGLE_OAUTH_USERINFO_URL: str
    GOOGLE_OAUTH_SCOPES: list[str]


CONFIG_VALUES = ConfigValues(
    GOOGLE_OAUTH_AUTHORIZE_URL="https://accounts.google.com/o/oauth2/auth",
    GOOGLE_OAUTH_TOKEN_URL="https://accounts.google.com/o/oauth2/token",
    GOOGLE_OAUTH_USERINFO_URL="https://www.googleapis.com/oauth2/v3/userinfo",
    GOOGLE_OAUTH_SCOPES=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
)


@dataclass(frozen=True)
class Config:
    DB_URL: str
    GOOGLE_OAUTH_CLIENT_ID: str  # TODO: For OAuth: rotate before deployment
    GOOGLE_OAUTH_CLIENT_SECRET: str  # For OAuth: rotate before deployment
    GOOGLE_OAUTH_AUTHORIZE_URL: str
    GOOGLE_OAUTH_TOKEN_URL: str
    GOOGLE_OAUTH_USERINFO_URL: str
    GOOGLE_OAUTH_SCOPES: list[str]
    SECRET_KEY: str


@cache
def get_config() -> Config:
    config_source: Mapping[str, str]

    if os.environ.get("SECRET_KEY"):
        logging.debug("Retreiving config from environment variables")
        config_source = os.environ
    else:
        logging.debug("Retreiving config from disk")
        with open(SECRETS_PATH) as f:
            secrets = json.load(f)

        config_source = secrets

    return Config(
        GOOGLE_OAUTH_CLIENT_ID=config_source.get(
            "GOOGLE_OAUTH_CLIENT_ID", "--NOT-IN-SECRETS--"
        ),
        GOOGLE_OAUTH_CLIENT_SECRET=config_source.get(
            "GOOGLE_OAUTH_CLIENT_SECRET", "--NOT-IN-SECRETS--"
        ),
        DB_URL=config_source.get("DB_URL", "--NOT-IN-SECRETS--"),
        GOOGLE_OAUTH_AUTHORIZE_URL=CONFIG_VALUES.GOOGLE_OAUTH_AUTHORIZE_URL,
        GOOGLE_OAUTH_TOKEN_URL=CONFIG_VALUES.GOOGLE_OAUTH_TOKEN_URL,
        GOOGLE_OAUTH_USERINFO_URL=CONFIG_VALUES.GOOGLE_OAUTH_USERINFO_URL,
        GOOGLE_OAUTH_SCOPES=CONFIG_VALUES.GOOGLE_OAUTH_SCOPES,
        SECRET_KEY=config_source.get("SECRET_KEY", "--NOT-IN-SECRETS--"),
    )
