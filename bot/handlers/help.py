from collections.abc import Callable

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("help"))
async def help_handler(message: Message, tr: Callable[..., str]) -> None:
    await message.answer(tr("help"))
