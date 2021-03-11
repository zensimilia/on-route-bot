import json
from typing import Union

from aiogram.types.inline_keyboard import (InlineKeyboardButton,
                                           InlineKeyboardMarkup)
from aiogram.utils.callback_data import CallbackData
from cron_descriptor import Options, get_description

from app.keyboards.inline_route import cd_routes
from app.utils import uchar

cd_schedules = CallbackData('schedules_menu', 'action', 'schedule_id')
cd_schedule_days = CallbackData("shedule", "days")


def kb_schedule_list(schedules: Union[dict, None], route_id: int) -> InlineKeyboardMarkup:
    buttons = list()
    options = Options()
    options.locale_code = 'ru_RU'
    options.use_24hour_time_format = True
    if schedules.count():
        for schedule in schedules:
            cron_object = json.loads(schedule.schedule)
            cron_string = f"{cron_object['minute']} {cron_object['hour']} * * {cron_object['day_of_week']}"
            description = get_description(cron_string, options)
            buttons.append([
                InlineKeyboardButton(
                    f'{description}',
                    callback_data=cd_schedules.new('select', schedule.id)
                ),
            ])
    buttons.append(
        [
            InlineKeyboardButton(
                f'{uchar.BACK_ARROW} Назад',
                callback_data=cd_routes.new(action='select', route_id=route_id)),
            InlineKeyboardButton(
                f'{uchar.NEW} Добавить',
                callback_data=cd_schedules.new('add', False)),

        ]
    )
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def kb_schedule_days() -> InlineKeyboardMarkup:
    """
    Display keyboard with days of week choice.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Ежедневно', callback_data=cd_schedule_days.new(days="*"))
            ],
            [
                InlineKeyboardButton(
                    'Рабочие', callback_data=cd_schedule_days.new(days="1-5")),
                InlineKeyboardButton(
                    'Выходные', callback_data=cd_schedule_days.new(days="6-0"))
            ],
            [
                InlineKeyboardButton(
                    'Пн', callback_data=cd_schedule_days.new(days=(1))),
                InlineKeyboardButton(
                    'Вт', callback_data=cd_schedule_days.new(days=(2))),
                InlineKeyboardButton(
                    'Ср', callback_data=cd_schedule_days.new(days=(3))),
                InlineKeyboardButton(
                    'Чт', callback_data=cd_schedule_days.new(days=(4))),
                InlineKeyboardButton(
                    'Пт', callback_data=cd_schedule_days.new(days=(5))),
                InlineKeyboardButton(
                    'Сб', callback_data=cd_schedule_days.new(days=(6))),
                InlineKeyboardButton(
                    'Вс', callback_data=cd_schedule_days.new(days=(0)))
            ]
        ]
    )
