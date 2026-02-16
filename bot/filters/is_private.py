from aiogram.filters import BaseFilter
from aiogram.enums import ChatType


class IsPrivate(BaseFilter):
    async def __call__(self, event, data) -> bool:
        chat = data.get("event_chat")
        return bool(chat and chat.type == ChatType.PRIVATE)
