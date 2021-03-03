from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateRoute(StatesGroup):
    """
    State class for creating route process.
    """

    name = State()
    url = State()


class CreateSchedule(StatesGroup):
    """
    State class for creating schedule for route.
    """

    time = State()
    days = State()
