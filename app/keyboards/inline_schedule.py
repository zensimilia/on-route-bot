import json
from typing import Union

from aiogram.types.inline_keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.callback_data import CallbackData

from app.keyboards.inline_route import cd_routes
from app.utils import uchar, cronity
from app.types import DayOfWeek

cd_schedules = CallbackData(
    'schedules_menu', 'action', 'schedule_id', 'route_id'
)
cd_schedule_days = CallbackData('schedule_days', 'days')
cd_schedule_times = CallbackData('schedule_time', 'time', sep='|')  # fixed sep


def kb_schedule_show(
    schedule_id: int, route_id: int, is_active: bool
) -> InlineKeyboardMarkup:
    """Display keyboard with actions for single schedule."""
    status = uchar.BELL if not is_active else uchar.BELL_STROKE
    toggle = 'Отключить уведомления' if is_active else 'Включить уведомления'
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{status} {toggle}',
                    callback_data=cd_schedules.new(
                        action='toggle',
                        schedule_id=schedule_id,
                        route_id=False,
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.WASTEBASKET} Удалить',
                    callback_data=cd_schedules.new(
                        action='delete',
                        schedule_id=schedule_id,
                        route_id=route_id,
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cd_routes.new(
                        action='schedule', route_id=route_id
                    ),
                ),
            ],
        ]
    )


def kb_schedule_list(
    schedules: Union[list, None], route_id: int
) -> InlineKeyboardMarkup:
    """Display keyboard with list of all schedules."""
    buttons = list()
    if schedules is not None:
        for schedule in schedules:
            cron = json.loads(schedule.schedule)
            readable = cronity.humanize(cron)
            buttons.append(
                [
                    InlineKeyboardButton(
                        f'{readable}',
                        callback_data=cd_schedules.new(
                            'select', schedule.id, False
                        ),
                    ),
                ]
            )
    buttons.append(
        [
            InlineKeyboardButton(
                f'{uchar.BACK_ARROW} Назад',
                callback_data=cd_routes.new(action='select', route_id=route_id),
            ),
            InlineKeyboardButton(
                f'{uchar.NEW} Добавить',
                callback_data=cd_schedules.new('add', False, route_id=route_id),
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_schedule_times() -> InlineKeyboardMarkup:
    """Display keyboard with list of times."""
    times = list()
    group = list()
    for i in range(0, 24):
        group.append(
            InlineKeyboardButton(
                f'{i}:00', callback_data=cd_schedule_times.new(time=f'{i}:00')
            )
        )
        if len(group) == 6:
            times.append(group.copy())
            group.clear()
    return InlineKeyboardMarkup(inline_keyboard=times)


def kb_schedule_days() -> InlineKeyboardMarkup:
    """Display keyboard with days of week choice."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    DayOfWeek.EVERY.title,
                    callback_data=cd_schedule_days.new(
                        days=DayOfWeek.EVERY.cron
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    DayOfWeek.WORK.title,
                    callback_data=cd_schedule_days.new(
                        days=DayOfWeek.WORK.cron
                    ),
                ),
                InlineKeyboardButton(
                    DayOfWeek.END.title,
                    callback_data=cd_schedule_days.new(days=DayOfWeek.END.cron),
                ),
            ],
            [
                InlineKeyboardButton(
                    DayOfWeek.MON.short,
                    callback_data=cd_schedule_days.new(days=DayOfWeek.MON.cron),
                ),
                InlineKeyboardButton(
                    DayOfWeek.TUE.short,
                    callback_data=cd_schedule_days.new(days=DayOfWeek.TUE.cron),
                ),
                InlineKeyboardButton(
                    DayOfWeek.WED.short,
                    callback_data=cd_schedule_days.new(days=DayOfWeek.WED.cron),
                ),
                InlineKeyboardButton(
                    DayOfWeek.THU.short,
                    callback_data=cd_schedule_days.new(days=DayOfWeek.THU.cron),
                ),
                InlineKeyboardButton(
                    DayOfWeek.FRI.short,
                    callback_data=cd_schedule_days.new(days=DayOfWeek.FRI.cron),
                ),
                InlineKeyboardButton(
                    DayOfWeek.SAT.short,
                    callback_data=cd_schedule_days.new(days=DayOfWeek.SAT.cron),
                ),
                InlineKeyboardButton(
                    DayOfWeek.SUN.short,
                    callback_data=cd_schedule_days.new(days=DayOfWeek.SUN.cron),
                ),
            ],
        ]
    )
