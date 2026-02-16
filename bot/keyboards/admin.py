from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Stats", callback_data="admin:stats")],
            [InlineKeyboardButton(text="Refresh", callback_data="admin:stats")],
        ]
    )
