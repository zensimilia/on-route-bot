from aiogram import types
from aiogram.dispatcher import FSMContext

from app.db import db_session
from app.models import User, Route, Schedule
from app.utils import uchar
from sqlalchemy import func

WELCOME_TEXT = (
    'Чтобы начать пользоваться ботом, необходимо создать первый маршрут и '
    'настроить для него расписание уведомлений. Вот несколько полезных команд:'
    '\n'
    '\n/routes - список ваших маршрутов'
    '\n/routeadd - добавить новый маршрут'
    '\n'
    '\n/help - помощь'
    '\n/settings - настройки'
    '\n/about - информация о боте'
    '\n'
    '\n/cancel - отменить текущую команду'
)

ABOUT_TEXT = (
    'Привет! Я бот, который поможет тебе быть в курсе дорожной обстановки '
    'на твоем маршруте. Я показываю время в пути по маршруту, прогноз погоды и '
    'карту с дорожной ситуацией. Ты можешь добавить столько маршрутов, сколько '
    'тебе потребуется, добавить для них уведомления и я буду присылать тебе '
    'сообщения с обстановкой в удобное для тебя время. Я пока работаю только с '
    'Yandex Maps. Надеюсь этот сервис тебе подходит. Удачи на дорогах!'
    '\n\n'
    '<b>Контакты</b>'
    '\nПо вопросам и предложениям пиши @zensimilia.'
    '\n\n'
    '<b>Статистика</b>'
    '\nПользователи: %(users)s'
    '\nМаршруты: %(routes)s'
    '\nУведомления: %(schedules)s'
)

HELP_TEXT = 'Soon...'


async def cmd_start(message: types.Message):
    """Show welcome message and register user.

    :param obj message: Message object.
    """
    with db_session() as db:
        user = db.query(User).filter(User.uid.__eq__(message.from_user.id))
        if not user:
            new_user = User(
                uid=message.from_user.id, username=message.from_user.username
            )
            db.add(new_user)
    await message.answer(WELCOME_TEXT)


async def cmd_about(message: types.Message):
    """Show information about bot."""
    stat = dict()
    with db_session() as db:
        stat['users'] = db.query(func.count(User.id)).scalar()
        stat['routes'] = db.query(func.count(Route.id)).scalar()
        stat['schedules'] = db.query(func.count(Schedule.id)).scalar()

    await message.answer(ABOUT_TEXT % stat)


async def cmd_help(message: types.Message):
    """Show information about bot."""
    await message.answer(HELP_TEXT)


async def cmd_cancel(message: types.Message, state: FSMContext):
    """Command to cancel any current state."""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            f'Нет активных комманд, чтобы их отменять {uchar.SHRUGGING}'
        )
        return
    await state.finish()
    await message.answer(
        f'Команда отменена {uchar.OK_HAND}',
        reply_markup=types.ReplyKeyboardRemove(),
    )
