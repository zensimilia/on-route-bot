from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import app.utils.uchar as uchar


cd_settings = CallbackData("settings_menu", "action", "data")
cb_cancel = cd_settings.new(action='cancel', data='void')
btn_cancel = InlineKeyboardButton('Отмена', callback_data=cb_cancel)


def kb_settings() -> InlineKeyboardMarkup:
    """
    Main keyboard for `/settings` command.
    """
    cb_tz = cd_settings.new(action='tz', data='void')
    tz = InlineKeyboardButton(
        f'{uchar.CLOCK} Часовой пояс', callback_data=cb_tz)
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(tz)
    inline_kb.add(btn_cancel)
    return inline_kb


def kb_settings_user_location() -> ReplyKeyboardMarkup:
    """
    Keyboard for get user location.
    """
    reply_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    geo = KeyboardButton(
        text="Отправить местоположение",
        request_location=True)
    reply_kb.add(geo)
    return reply_kb
