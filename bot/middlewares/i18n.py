from aiogram import BaseMiddleware

from ..db import Database
from ..i18n import get_translator, normalize_locale


class LocaleMiddleware(BaseMiddleware):
    def __init__(self, default_locale: str, db: Database | None = None) -> None:
        self._default_locale = normalize_locale(default_locale)
        self._db = db

    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")
        locale = self._default_locale
        if user and user.language_code:
            locale = normalize_locale(user.language_code)

        if self._db and user:
            saved_locale = await self._db.get_user_language(user.id)
            if saved_locale:
                locale = normalize_locale(saved_locale)

        data["locale"] = locale
        data["tr"] = get_translator(locale)
        return await handler(event, data)
