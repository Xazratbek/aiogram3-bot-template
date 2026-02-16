from collections.abc import Callable

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..data.constants import APP_NAME
from ..keyboards.settings import settings_kb


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, tr: Callable[..., str]) -> None:
    text = tr("start", app_name=APP_NAME)
    await message.answer(text, reply_markup=settings_kb(tr))
