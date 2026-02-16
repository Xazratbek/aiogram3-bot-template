from collections.abc import Callable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def settings_kb(tr: Callable[..., str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=tr("settings_button"), callback_data="settings:open")],
        ]
    )


def settings_menu_kb(tr: Callable[..., str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=tr("settings_language_button"),
                    callback_data="settings:lang",
                )
            ],
        ]
    )
