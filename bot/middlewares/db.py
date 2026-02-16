from aiogram import BaseMiddleware

from ..db import Database


class DbMiddleware(BaseMiddleware):
    def __init__(self, db: Database) -> None:
        self._db = db

    async def __call__(self, handler, event, data):
        data["db"] = self._db
        return await handler(event, data)
