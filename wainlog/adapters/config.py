import json
import logging
import os
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Mapping

SECRETS_PATH = Path(__file__).resolve().parents[2] / "wainlog-secrets.json"


@dataclass(frozen=True)
class Config:
    DB_URL: str
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
        DB_URL=config_source.get("DB_URL", "--NOT-IN-SECRETS--"),
        SECRET_KEY=config_source.get("SECRET_KEY", "--NOT-IN-SECRETS--"),
    )
