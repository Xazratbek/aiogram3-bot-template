from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    log_level: str = "INFO"
    admin_ids: tuple[int, ...] = ()
    db_path: str = "storage/bot.db"
    default_locale: str = "uz"
    flood_limit: float = 0.0

    @property
    def db_dir(self) -> Path:
        return Path(self.db_path).parent


def _parse_admin_ids(raw: str | None) -> tuple[int, ...]:
    if not raw:
        return ()
    parts: Iterable[str] = (piece.strip() for piece in raw.split(","))
    ids: list[int] = []
    for part in parts:
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            continue
    return tuple(dict.fromkeys(ids))


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS"))
    db_path = os.getenv("DB_PATH", "storage/bot.db")
    default_locale = os.getenv("DEFAULT_LOCALE", "uz").lower()
    flood_limit = float(os.getenv("FLOOD_LIMIT", "0") or "0")
    return Settings(
        bot_token=token,
        log_level=log_level,
        admin_ids=admin_ids,
        db_path=db_path,
        default_locale=default_locale,
        flood_limit=flood_limit,
    )
