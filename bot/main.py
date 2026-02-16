import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import load_settings
from .db import Database
from .handlers import get_routers
from .logging_config import setup_logging
from .middlewares import DbMiddleware, LocaleMiddleware, ThrottlingMiddleware, UserMiddleware
from .utils.commands import set_bot_commands

logger = logging.getLogger(__name__)


async def notify_admins(bot: Bot, admin_ids: tuple[int, ...]) -> None:
    if not admin_ids:
        return
    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, "Bot ishga tushdi /start")
        except Exception:
            logger.exception("Failed to notify admin %s", admin_id)


async def main() -> None:
    settings = load_settings()
    setup_logging(settings.log_level)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    db = Database(settings.db_path)
    await db.connect()
    await db.init()

    dp = Dispatcher()
    dp["settings"] = settings
    dp.update.middleware(ThrottlingMiddleware(settings.flood_limit))
    dp.update.middleware(DbMiddleware(db))
    dp.update.middleware(UserMiddleware(db, set(settings.admin_ids)))
    dp.update.middleware(LocaleMiddleware(settings.default_locale, db))
    dp.include_routers(*get_routers())

    await set_bot_commands(bot, settings.admin_ids)
    await notify_admins(bot, settings.admin_ids)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
