from time import monotonic

from aiogram import BaseMiddleware


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float) -> None:
        self._rate_limit = rate_limit
        self._last_time: dict[int, float] = {}

    async def __call__(self, handler, event, data):
        if self._rate_limit <= 0:
            return await handler(event, data)

        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        now = monotonic()
        last_time = self._last_time.get(user.id)
        if last_time is not None and now - last_time < self._rate_limit:
            return None

        self._last_time[user.id] = now
        return await handler(event, data)
