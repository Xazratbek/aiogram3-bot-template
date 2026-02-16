from collections.abc import Callable

from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..keyboards.settings import settings_menu_kb


router = Router()


@router.callback_query(F.data == "settings:open")
async def settings_open_handler(
    callback: CallbackQuery,
    tr: Callable[..., str],
) -> None:
    if callback.message:
        await callback.message.edit_text(
            tr("settings_title"),
            reply_markup=settings_menu_kb(tr),
        )
    await callback.answer()
