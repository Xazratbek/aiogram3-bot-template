from collections.abc import Callable

from aiogram import F, Router
from aiogram.types import Message

from ..i18n.messages import MESSAGES
from ..keyboards.settings import settings_menu_kb

router = Router()

SETTINGS_BUTTONS = tuple(
    {data["settings_button"] for data in MESSAGES.values() if "settings_button" in data}
)


@router.message(F.text.in_(SETTINGS_BUTTONS))
async def settings_open_handler(
    message: Message,
    tr: Callable[..., str],
) -> None:
    await message.answer(
        tr("settings_title"),
        reply_markup=settings_menu_kb(tr),
    )
