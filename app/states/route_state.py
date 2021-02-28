from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateRoute(StatesGroup):
    """
    State class for creating route process.
    """

    name = State()
    url = State()
