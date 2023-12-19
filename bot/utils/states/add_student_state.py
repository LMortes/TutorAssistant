from aiogram.dispatcher.filters.state import State, StatesGroup


class AddStudent(StatesGroup):
    add_student_state = State()
    add_student_id = State()
    add_student_name = State()
    add_student_subject = State()
    add_student_class = State()
    add_student_purpose = State()
    add_student_price = State()
    add_student_transfer = State()
    add_student_phone = State()
    add_student_platform = State()
    add_student_platform_nick = State()
    add_student_timezone = State()