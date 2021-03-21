import json

from aiogram import types
from aiogram.dispatcher import FSMContext

import app.utils.uchar as uchar
from app.keyboards.inline_schedule import *
from app.models import Route, Schedule
from app.states import CreateSchedule


async def schedule_list(cb: types.CallbackQuery, callback_data: dict):
    """
    List all schedules for specific route.
    """
    route_id = callback_data['route_id']
    route = Route.get_by_id(route_id)
    schedules = route.schedules
    await cb.message.edit_text(f'Настройка уведомлений для маршрута <b>{route.name}</b>.', reply_markup=kb_schedule_list(schedules, route_id))
    await cb.answer()


async def schedule_add(cb: types.CallbackQuery, callback_data: dict):
    await cb.message.edit_text(
        '<code>1/2</code> Пожалуйста, выберите желаемое время уведомления о маршруте.',
        reply_markup=kb_schedule_times()
    )
    CreateSchedule.route_id = callback_data['route_id']
    await CreateSchedule.time.set()
    await cb.answer()


async def schedule_add_time(cb: types.CallbackQuery, callback_data: dict, state: FSMContext):
    time = callback_data['time']
    await state.update_data(time=time)
    await CreateSchedule.next()
    await cb.message.edit_text('<code>2/2</code> Теперь выберите дни, в которые надо получать уведомления.', reply_markup=kb_schedule_days())


async def schedule_add_days(cb: types.CallbackQuery, state: FSMContext):
    cb_data = cd_schedule_days.parse(cb.data)
    await state.update_data(days=cb_data['days'])
    state_data = await state.get_data()
    minute = state_data['time'].split(':')[-1]
    hour = state_data['time'].split(':')[0]
    day_of_week = state_data['days']
    schedule = {
        'minute': minute,
        'hour': hour,
        'day_of_week': day_of_week,
    }
    route = Route.get_by_id(CreateSchedule.route_id)
    Schedule.create(route=route, schedule=json.dumps(schedule), is_active=True)
    await state.finish()
    await cb.message.delete_reply_markup()
    await cb.message.answer(f'Уведомление добавлено {uchar.OK_HAND}')
    await cb.answer()


async def schedule_add_error(message: types.Message):
    """
    Handle errors in create shcedule process.
    """
    await message.answer('Не понимаю этот формат. Попробуйте еще раз или введите команду отмены /cancel.')
