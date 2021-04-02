import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from app.keyboards import inline_schedule
from app.models import Route, Schedule
from app.states import CreateSchedule
from app.utils import uchar


async def schedule_list(cb: types.CallbackQuery, callback_data: dict):
    """List all schedules for specific route."""
    route_id = callback_data['route_id']
    route = Route.get_by_id(route_id)
    schedules = route.schedules
    await cb.message.edit_text(
        f'Настройка уведомлений для маршрута <b>{route.name}</b>.',
        reply_markup=inline_schedule.kb_schedule_list(schedules, route_id),
    )
    await cb.answer()


async def schedule_add(cb: types.CallbackQuery, callback_data: dict):
    await cb.message.edit_text(
        '<code>1/2</code> Пожалуйста, '
        'выберите желаемое время уведомления о маршруте.',
        reply_markup=inline_schedule.kb_schedule_times(),
    )
    CreateSchedule.route_id = callback_data['route_id']
    await CreateSchedule.time.set()
    await cb.answer()


async def schedule_add_time(
    cb: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    await state.update_data(time=callback_data['time'])
    await CreateSchedule.next()
    await cb.message.edit_text(
        '<code>2/2</code> Теперь выберите дни, '
        'в которые надо получать уведомления.',
        reply_markup=inline_schedule.kb_schedule_days(),
    )


async def schedule_add_days(
    cb: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    """Save schedule data to database."""
    await state.update_data(days=callback_data['days'])
    state_data = await state.get_data()
    time = state_data['time'].split(':')
    day_of_week = state_data['days']
    schedule = {
        'hour': time[0],
        'minute': time[1],
        'day_of_week': day_of_week,
    }
    route = Route.get_by_id(CreateSchedule.route_id)
    Schedule.create(route=route, schedule=json.dumps(schedule), is_active=True)
    await cb.message.delete_reply_markup()
    await cb.message.edit_text(
        f'Уведомление добавлено {uchar.OK_HAND} '
        '\nВернуться к списку маршрутов /routes'
    )
    await cb.answer()
    await state.finish()


async def schedule_add_error(message: types.Message):
    """Handle errors in create shcedule process."""
    await message.answer(
        'Не понимаю этот формат. Попробуйте еще раз '
        'или введите команду отмены /cancel.'
    )
