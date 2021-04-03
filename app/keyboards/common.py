from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_button() -> ReplyKeyboardMarkup:
    """Returns markup of cancel button."""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton('Отмена')],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
