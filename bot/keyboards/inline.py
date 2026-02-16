from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def github_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="GitHub", url="https://github.com")],
        ]
    )
