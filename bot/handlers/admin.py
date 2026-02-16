from collections.abc import Callable

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from ..db import Database
from ..filters import IsAdmin
from ..keyboards.admin import admin_menu_kb


router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("admin"))
async def admin_handler(message: Message, tr: Callable[..., str]) -> None:
    await message.answer(tr("admin_panel"), reply_markup=admin_menu_kb())


@router.callback_query(F.data == "admin:stats")
async def admin_stats_handler(
    callback: CallbackQuery,
    db: Database,
    tr: Callable[..., str],
) -> None:
    count = await db.count_users()
    text = tr("users_count", count=count)
    await callback.answer()
    if callback.message:
        await callback.message.edit_text(text, reply_markup=admin_menu_kb())
