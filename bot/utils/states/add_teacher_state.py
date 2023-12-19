from aiogram.dispatcher.filters.state import State, StatesGroup


class AddTeacher(StatesGroup):
    get_user_id = State()
    get_fio = State()
    get_subject = State()