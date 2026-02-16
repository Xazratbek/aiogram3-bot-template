from collections.abc import Iterable

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


DEFAULT_COMMANDS = [
    BotCommand(command="start", description="Botni ishga tushirish"),
    BotCommand(command="help", description="Yordam"),
    BotCommand(command="lang", description="Tilni o'zgartirish"),
]

ADMIN_COMMANDS = [
    *DEFAULT_COMMANDS,
    BotCommand(command="admin", description="Admin panel"),
]


async def set_bot_commands(bot: Bot, admin_ids: Iterable[int] | None = None) -> None:
    await bot.set_my_commands(DEFAULT_COMMANDS)
    if not admin_ids:
        return
    for admin_id in admin_ids:
        await bot.set_my_commands(
            ADMIN_COMMANDS,
            scope=BotCommandScopeChat(chat_id=admin_id),
        )
