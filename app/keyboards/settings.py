from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData

from app.utils import uchar

cd_settings = CallbackData('settings_menu', 'action', 'data')
cb_cancel = cd_settings.new(action='cancel', data='void')
btn_cancel = InlineKeyboardButton('Отмена', callback_data=cb_cancel)


def kb_settings() -> InlineKeyboardMarkup:
    """Return keyboard with list of settings."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.GLOBE} Часовой пояс',
                    callback_data=cd_settings.new(action='tz', data=False),
                )
            ],
        ]
    )


def kb_settings_tz() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Изменить часовой пояс',
                    callback_data=cd_settings.new(
                        action='tz-change', data=False
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cd_settings.new(action='list', data=False),
                )
            ],
        ]
    )


def kb_settings_back() -> InlineKeyboardMarkup:
    """Keyboard for get user back to list of settings."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cd_settings.new(action='list', data=False),
                )
            ],
        ]
    )
