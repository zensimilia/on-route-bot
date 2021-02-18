from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


async def something_went_wrong(messsage: types.Message, error: str = None):
    """
    Show error message when exception is raised.

    :param obj message: Message object.
    :param obj error: Error object with `__str__` method.
    """
    if error is None:
        error = 'Что-то пошло не так!'
    text = f'<b>{error}</b> \nПопробуйте позже или обратитесь к автору бота (ссылка в профиле).'
    await messsage.answer(text)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(
        cmd_cancel,
        Text(equals="отмена",
             ignore_case=True),
        state="*")
