from collections.abc import Callable

from aiogram import F, Router
from aiogram.types import Message


router = Router()


@router.message(F.text & ~F.text.startswith("/"))
async def echo_handler(message: Message, tr: Callable[..., str]) -> None:
    await message.answer(f"{tr('echo_prefix')} {message.text}")
