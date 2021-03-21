import json
from typing import Union

from aiogram.types.inline_keyboard import (InlineKeyboardButton,
                                           InlineKeyboardMarkup)
from aiogram.utils.callback_data import CallbackData

from app.keyboards.inline_route import cd_routes
from app.utils import uchar, cronity

cd_schedules = CallbackData(
    'schedules_menu', 'action', 'schedule_id', 'route_id')
cd_schedule_days = CallbackData('schedule_days', 'days')
cd_schedule_times = CallbackData('schedule_time', 'time')


def kb_schedule_list(schedules: Union[dict, None], route_id: int) -> InlineKeyboardMarkup:
    buttons = list()
    if schedules.count():
        for schedule in schedules:
            cron = json.loads(schedule.schedule)
            readable = cronity.humanize(cron)
            buttons.append([
                InlineKeyboardButton(
                    f'{readable}',
                    callback_data=cd_schedules.new(
                        'select', schedule.id, False)
                ),
            ])
    buttons.append(
        [
            InlineKeyboardButton(
                f'{uchar.BACK_ARROW} Назад',
                callback_data=cd_routes.new(action='select', route_id=route_id)),
            InlineKeyboardButton(
                f'{uchar.NEW} Добавить',
                callback_data=cd_schedules.new('add', False, route_id=route_id)),

        ]
    )
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def kb_schedule_times() -> InlineKeyboardMarkup:
    """
    Display keyboard with list of times.
    """
    times = list()
    group = list()
    for i in range(0, 24):
        group.append(
            InlineKeyboardButton(
                f'{i}:00', callback_data=cd_schedule_times.new(time=f'{i}.00')
            )
        )
        if len(group) == 6:
            times.append(group.copy())
            group.clear()
    return InlineKeyboardMarkup(
        inline_keyboard=times
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
