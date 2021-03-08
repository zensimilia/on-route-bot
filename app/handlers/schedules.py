import json

from aiogram import types
from aiogram.dispatcher import FSMContext

import app.utils.uchar as uchar
from app.keyboards.inline_schedule import *
from app.models import Route, Schedule
from app.states import CreateSchedule


async def schedule_add(cb: types.CallbackQuery, callback_data: dict):
    await cb.message.answer(
        '<code>1/2</code> Пожалуйста, введите желаемое время уведомления о маршруте в формате <code>ЧЧ:ММ</code>.')
    CreateSchedule.route_id = callback_data['route_id']
    await CreateSchedule.time.set()
    await cb.answer()


async def schedule_add_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await CreateSchedule.next()
    await message.answer('<code>2/2</code> Теперь выберите дни, в которые надо получать уведомления.', reply_markup=kb_schedule_days())


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
