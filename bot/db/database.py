from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import aiosqlite


@dataclass(slots=True)
class User:
    user_id: int
    username: str | None
    full_name: str
    language_code: str | None
    is_admin: bool


class Database:
    def __init__(self, path: str) -> None:
        self._path = path
        self._conn: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        Path(self._path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = await aiosqlite.connect(self._path)
        await self._conn.execute("PRAGMA foreign_keys = ON")

    async def close(self) -> None:
        if self._conn is None:
            return
        await self._conn.close()
        self._conn = None

    async def init(self) -> None:
        if self._conn is None:
            raise RuntimeError("Database is not connected")
        await self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT NOT NULL,
                language_code TEXT,
                is_admin INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await self._conn.commit()

    async def upsert_user(
        self,
        *,
        user_id: int,
        username: str | None,
        full_name: str,
        language_code: str | None,
        is_admin: bool,
    ) -> None:
        if self._conn is None:
            raise RuntimeError("Database is not connected")
        await self._conn.execute(
            """
            INSERT INTO users (user_id, username, full_name, language_code, is_admin)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                full_name=excluded.full_name,
                language_code=CASE
                    WHEN users.language_code IS NULL THEN excluded.language_code
                    ELSE users.language_code
                END,
                is_admin=excluded.is_admin
            """,
            (user_id, username, full_name, language_code, int(is_admin)),
        )
        await self._conn.commit()

    async def set_user_language(self, user_id: int, language_code: str) -> None:
        if self._conn is None:
            raise RuntimeError("Database is not connected")
        await self._conn.execute(
            "UPDATE users SET language_code = ? WHERE user_id = ?",
            (language_code, user_id),
        )
        await self._conn.commit()

    async def get_user_language(self, user_id: int) -> str | None:
        if self._conn is None:
            raise RuntimeError("Database is not connected")
        async with self._conn.execute(
            "SELECT language_code FROM users WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

    async def count_users(self) -> int:
        if self._conn is None:
            raise RuntimeError("Database is not connected")
        async with self._conn.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return int(row[0]) if row else 0

    async def get_admin_ids(self) -> list[int]:
        if self._conn is None:
            raise RuntimeError("Database is not connected")
        async with self._conn.execute(
            "SELECT user_id FROM users WHERE is_admin = 1"
        ) as cursor:
            rows = await cursor.fetchall()
        return [int(row[0]) for row in rows]
