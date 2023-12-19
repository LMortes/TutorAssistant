from aiogram.dispatcher.filters.state import State, StatesGroup


class AddLesson(StatesGroup):
    add_lesson_state = State()
    add_week_day = State()
    add_lesson_time = State()