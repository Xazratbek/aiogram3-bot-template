from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    text = (
        "Yordam bo'limi:\n"
        "- /start botni qayta ishga tushirish\n"
        "- /help ushbu xabar\n"
        "\n"
        "Oddiy xabar yuborsangiz, bot uni aks ettiradi."
    )
    await message.answer(text)
