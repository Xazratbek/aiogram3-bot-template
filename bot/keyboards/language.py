from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

LANG_LABELS = {
    "uz": "🇺🇿 O'zbek",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}


def language_kb(current_locale: str | None) -> InlineKeyboardMarkup:
    buttons = []
    for code, label in LANG_LABELS.items():
        prefix = "✅ " if current_locale == code else ""
        buttons.append(
            InlineKeyboardButton(
                text=f"{prefix}{label}",
                callback_data=f"lang:{code}",
            )
        )
    keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
