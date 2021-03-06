from aiogram.utils.callback_data import CallbackData
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

cd_schedule_days = CallbackData("shedule", "days")


def kb_schedule_days() -> InlineKeyboardMarkup:
    cb_week = cd_schedule_days.new(days="0-6")
    cb_work = cd_schedule_days.new(days="0-4")
    cb_weekend = cd_schedule_days.new(days="5-6")

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Ежедневно', callback_data=cb_week)
            ],
            [
                InlineKeyboardButton('Рабочие', callback_data=cb_work),
                InlineKeyboardButton('Выходные', callback_data=cb_weekend)
            ],
            [
                InlineKeyboardButton(
                    'Пн', callback_data=cd_schedule_days.new(days=(0))),
                InlineKeyboardButton(
                    'Вт', callback_data=cd_schedule_days.new(days=(1))),
                InlineKeyboardButton(
                    'Ср', callback_data=cd_schedule_days.new(days=(2))),
                InlineKeyboardButton(
                    'Чт', callback_data=cd_schedule_days.new(days=(3))),
                InlineKeyboardButton(
                    'Пт', callback_data=cd_schedule_days.new(days=(4))),
                InlineKeyboardButton(
                    'Сб', callback_data=cd_schedule_days.new(days=(5))),
                InlineKeyboardButton(
                    'Вс', callback_data=cd_schedule_days.new(days=(6)))
            ]
        ]
    )
