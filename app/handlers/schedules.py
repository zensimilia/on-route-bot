import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from app.keyboards import inline_schedule
from app.models import Route, Schedule
from app.states import CreateSchedule


async def schedule_list(cb: types.CallbackQuery, callback_data: dict):
    """List all schedules for specific route."""
    route = Route.get_by_id(callback_data['route_id'])
    schedules = route.schedules
    await cb.message.edit_text(
        f'Настройка уведомлений для маршрута <b>{route.name}</b>.',
        reply_markup=inline_schedule.kb_schedule_list(schedules, route.id),
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
    state_data = await state.get_data()
    time = state_data['time'].split(':')
    day_of_week = callback_data['days']
    cron = {
        'hour': time[0],
        'minute': time[1],
        'day_of_week': day_of_week,
    }
    route = Route.get_by_id(CreateSchedule.route_id)
    schedule = Schedule(route=route, schedule=json.dumps(cron), is_active=True)
    schedule.save()
    callback_data['route_id'] = route.id
    await state.finish()
    await cb.answer('Расписание уведомления добавлено')
    await schedule_list(cb, callback_data=callback_data)


async def schedule_select(cb: types.CallbackQuery, callback_data: dict):
    """Show single schedule."""
    schedule = Schedule.get_by_id(callback_data['schedule_id'])
    route = schedule.route
    await cb.message.edit_text(
        f'Редактирование уведомления для маршрута <b>{route.name}</b>',
        reply_markup=inline_schedule.kb_schedule_show(
            schedule.id, route.id, schedule.is_active
        ),
    )


async def schedule_toggle(cb: types.CallbackQuery, callback_data: dict):
    """Toggle is_active schedule property."""
    schedule = Schedule.get_by_id(callback_data['schedule_id'])
    schedule.is_active = not schedule.is_active
    schedule.save()
    alert_text = (
        'Уведомления включены'
        if schedule.is_active
        else 'Уведомления отключены'
    )
    await cb.answer(alert_text, show_alert=True)
    await cb.message.edit_reply_markup(
        inline_schedule.kb_schedule_show(
            schedule.id, schedule.route.id, schedule.is_active
        )
    )


async def schedule_delete(cb: types.CallbackQuery, callback_data: dict):
    """Delete schedule."""
    Schedule.get_by_id(callback_data['schedule_id']).delete_instance()
    await cb.answer('Расписание уведомления удалено', show_alert=True)
    await schedule_list(cb, callback_data)
