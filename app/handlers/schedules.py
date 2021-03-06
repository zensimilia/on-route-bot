import logging
import json

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

import app.utils.uchar as uchar
from app.keyboards.routes import *
from app.keyboards.inline_schedule import *
from app.models import Route, Schedule, schedule
from app.states import CreateSchedule


async def schedule_add(cb: types.CallbackQuery, route_id: int):
    await cb.message.answer(
        '<code>1/2</code> Пожалуйста, введите желаемое время уведомления о маршруте в формате <code>ЧЧ:ММ</code>.')
    CreateSchedule.route_id = route_id
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


async def process_callback_schedule():
    pass


def register_handlers_schedules(dp: Dispatcher):
    """
    Register schedule handlers in Dispatcher.
    """
    logging.info('Configuring schedule handlers...')
    dp.register_message_handler(
        schedule_add_time,
        is_time=True,
        state=CreateSchedule.time)
    dp.register_callback_query_handler(
        schedule_add_days,
        cd_schedule_days.filter(),
        state=CreateSchedule.days)
