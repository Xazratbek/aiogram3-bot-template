from collections.abc import Callable

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from ..db import Database
from ..i18n import get_translator, normalize_locale
from ..i18n.messages import MESSAGES
from ..keyboards.language import language_kb
from ..keyboards.settings import settings_menu_kb


router = Router()

SETTINGS_LANGUAGE_BUTTONS = tuple(
    {
        data["settings_language_button"]
        for data in MESSAGES.values()
        if "settings_language_button" in data
    }
)


@router.message(Command("lang"))
async def language_handler(message: Message, locale: str, tr: Callable[..., str]) -> None:
    await message.answer(tr("choose_language"), reply_markup=language_kb(locale))


@router.message(F.text.in_(SETTINGS_LANGUAGE_BUTTONS))
async def settings_language_handler(
    message: Message,
    locale: str,
    tr: Callable[..., str],
) -> None:
    await message.answer(tr("choose_language"), reply_markup=language_kb(locale))


@router.callback_query(F.data.startswith("lang:"))
async def set_language_handler(
    callback: CallbackQuery,
    db: Database,
) -> None:
    if not callback.from_user:
        return
    code = callback.data.split(":", maxsplit=1)[1]
    normalized = normalize_locale(code)
    await db.set_user_language(callback.from_user.id, normalized)

    tr = get_translator(normalized)
    await callback.answer(tr("language_set"))
    if callback.message:
        await callback.message.edit_text(
            tr("choose_language"),
            reply_markup=language_kb(normalized),
        )
        await callback.message.answer(
            tr("settings_title"),
            reply_markup=settings_menu_kb(tr),
        )
