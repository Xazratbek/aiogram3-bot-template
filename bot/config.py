from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    log_level: str = "INFO"


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    return Settings(bot_token=token, log_level=log_level)
