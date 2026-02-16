from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..data.constants import APP_NAME
from ..keyboards.reply import main_menu_kb


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    text = (
        f"Salom! {APP_NAME} ishga tushdi.\n"
        "Quyidagi tugmalar orqali yordam olishingiz mumkin."
    )
    await message.answer(text, reply_markup=main_menu_kb())
