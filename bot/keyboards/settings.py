from collections.abc import Callable

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def settings_kb(tr: Callable[..., str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=tr("settings_button"))]],
        resize_keyboard=True,
    )


def settings_menu_kb(tr: Callable[..., str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=tr("settings_language_button"))]],
        resize_keyboard=True,
    )
