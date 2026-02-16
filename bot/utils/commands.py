from aiogram import Bot
from aiogram.types import BotCommand


DEFAULT_COMMANDS = [
    BotCommand(command="start", description="Botni ishga tushirish"),
    BotCommand(command="help", description="Yordam"),
]


async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(DEFAULT_COMMANDS)
