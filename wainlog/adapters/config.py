import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

SECRETS_PATH = Path(__file__).resolve().parents[2] / "wainlog-secrets.json"
_config = None


@dataclass
class Config:
    DB_URL: str
    SECRET_KEY: str


def get_config():
    global _config

    if _config:
        return _config

    config_source: Mapping[str, str]

    if os.environ.get("SECRET_KEY"):
        logging.debug("Retreiving config from environment variables")
        config_source = os.environ
    else:
        logging.debug("Retreiving config from disk")
        with open(SECRETS_PATH) as f:
            secrets = json.load(f)

        config_source = secrets

    _config = Config(
        DB_URL=config_source.get("DB_URL", "--NOT-IN-SECRETS--"),
        SECRET_KEY=config_source.get("SECRET_KEY", "--NOT-IN-SECRETS--"),
    )

    return _config
