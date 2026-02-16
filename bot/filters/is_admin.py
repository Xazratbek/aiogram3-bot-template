from aiogram.filters import BaseFilter


class IsAdmin(BaseFilter):
    async def __call__(self, event, data) -> bool:
        user = data.get("event_from_user")
        settings = data.get("settings")
        if not user or not settings:
            return False
        return user.id in settings.admin_ids
