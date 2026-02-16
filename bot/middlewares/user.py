from aiogram import BaseMiddleware

from ..db import Database
from ..i18n import normalize_locale


class UserMiddleware(BaseMiddleware):
    def __init__(self, db: Database, admin_ids: set[int]) -> None:
        self._db = db
        self._admin_ids = admin_ids

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        if user:
            await self._db.upsert_user(
                user_id=user.id,
                username=user.username,
                full_name=user.full_name,
                language_code=normalize_locale(user.language_code),
                is_admin=user.id in self._admin_ids,
            )
        return await handler(event, data)
