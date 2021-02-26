from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_button() -> ReplyKeyboardMarkup:
    """
    Returns markup of cancel button.
    """
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True)
    cancel_button = KeyboardButton('Отмена')
    keyboard.add(cancel_button)
    return keyboard
