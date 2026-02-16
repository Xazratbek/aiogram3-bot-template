from aiogram import F, Router
from aiogram.types import Message


router = Router()


@router.message(F.text)
async def echo_handler(message: Message) -> None:
    await message.answer(message.text)
