from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeStudentInfo(StatesGroup):
    get_student_id = State()
    get_student_name = State()
    get_student_subject = State()
    get_student_class = State()
    get_student_purpose = State()
    get_student_price = State()
    get_student_transfer = State()
    get_student_phone = State()
    get_student_platform = State()
    get_student_nick = State()
    get_student_timezone = State()