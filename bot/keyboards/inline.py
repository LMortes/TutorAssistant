from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.mysql import db

ikb_auth = InlineKeyboardMarkup(row_width=1)

ikb_auth_button_teacher = InlineKeyboardButton(text='👨‍🏫 Я репетитор', callback_data='auth_teacher')
ikb_auth_button_student = InlineKeyboardButton(text='👦 Я ученик', callback_data='auth_student')

ikb_auth.add(ikb_auth_button_teacher).add(ikb_auth_button_student)


async def ikb_list_teachers(teachers_info):
    ikb_teachers_list = InlineKeyboardMarkup(row_width=1)

    for teacher in teachers_info:
        ikb_teacher_list_button = InlineKeyboardButton(text=f'{teacher[2]}', callback_data=f'list_teachers_{teacher[1]}')
        ikb_teachers_list.add(ikb_teacher_list_button)

    return ikb_teachers_list


async def ikb_list_students(students_info):
    ikb_students_list = InlineKeyboardMarkup(row_width=2)

    for student in students_info:
        ikb_student_list_button = InlineKeyboardButton(text=f'{student[2]}', callback_data=f'list_students_{student[1]}')
        ikb_students_list.insert(ikb_student_list_button)

    return ikb_students_list

async def ikb_teacher_info(teacher_id):
    ikb_settings_teacher = InlineKeyboardMarkup(row_width=1)

    ikb_change_fio_teacher_button = InlineKeyboardButton(text='⬅️ Назад', callback_data=f'teacher_info_back')

    ikb_settings_teacher.add(ikb_change_fio_teacher_button)

    return ikb_settings_teacher


async def ikb_student_info(student_id):
    ikb_settings_student = InlineKeyboardMarkup(row_width=1)

    ikb_settings_go_change = InlineKeyboardButton(text='⚙️ Управление', callback_data=f'manage_student_{student_id}')
    ikb_change_fio_student_button = InlineKeyboardButton(text='⬅️ Назад', callback_data=f'student_info_back')

    ikb_settings_student.add(ikb_settings_go_change).add(ikb_change_fio_student_button)

    return ikb_settings_student

async def generate_keyboard_add_student(student_info):
    ikb_add_student = InlineKeyboardMarkup(row_width=2)

    ikb_user_id_button = InlineKeyboardButton(text=f'{"🔴" if student_info["user_id"] is None else "✅"} ID', callback_data='add_student_id')
    ikb_name_button = InlineKeyboardButton(text=f'{"🔴" if student_info["name"] is None else "✅"} Имя ученика', callback_data='add_student_name')
    ikb_subject_button = InlineKeyboardButton(text=f'{"🔴" if student_info["subject"] is None else "✅"} Предмет', callback_data='add_student_subject')
    ikb_class_button = InlineKeyboardButton(text=f'{"🔴" if student_info["class_student"] is None else "✅"} Класс', callback_data='add_student_class')
    ikb_purpose_button = InlineKeyboardButton(text=f'{"🔴" if student_info["purpose"] is None else "✅"} Цель занятий', callback_data='add_student_purpose')
    ikb_price_button = InlineKeyboardButton(text=f'{"🔴" if student_info["price"] is None else "✅"} Цена', callback_data='add_student_price')
    ikb_transfer_button = InlineKeyboardButton(text=f'{"" if student_info["transfer"] is None else "✅"} Трансфер', callback_data='add_student_transfer')
    ikb_phone_button = InlineKeyboardButton(text=f'{"" if student_info["phone"] is None else "✅"} Телефон', callback_data='add_student_phone')
    ikb_platform_button = InlineKeyboardButton(text=f'{"🔴" if student_info["platform"] is None else "✅"} Платформа', callback_data='add_student_platform')
    ikb_platform_nick_button = InlineKeyboardButton(text=f'{"" if student_info["platform_nick"] is None else "✅"} Ник на платформе', callback_data='add_student_platform_nick')
    ikb_timezone_button = InlineKeyboardButton(text=f'{"" if student_info["timezone"] == "+0" else "✅"} ЧП (по умолчанию МСК)', callback_data='add_student_timezone')

    ikb_close_add_student_button = InlineKeyboardButton(text='❌ Отмена', callback_data='add_student_close')
    ikb_continue_add_student_button = InlineKeyboardButton(text='Продолжить', callback_data='add_student_continue')

    ikb_add_student\
        .add(ikb_user_id_button, ikb_name_button)\
        .add(ikb_subject_button, ikb_class_button)\
        .add(ikb_purpose_button, ikb_price_button)\
        .add(ikb_transfer_button, ikb_phone_button)\
        .add(ikb_platform_button, ikb_platform_nick_button)\
        .add(ikb_timezone_button)\
        .add(ikb_close_add_student_button, ikb_continue_add_student_button)

    return ikb_add_student


async def generate_keyboard_add_lesson(lesson_info):
    ikb_add_lesson = InlineKeyboardMarkup(row_width=2)

    ikb_add_lesson_button_week_day = InlineKeyboardButton(text=f'{"🔴" if lesson_info["week_day"] is None else "✅"} День недели', callback_data='add_lesson_week_day')
    ikb_add_lesson_button_lesson_time = InlineKeyboardButton(text=f'{"🔴" if lesson_info["lesson_time"] is None else "✅"} Время', callback_data='add_lesson_lesson_time')

    ikb_close_add_lesson_button = InlineKeyboardButton(text='❌ Отмена', callback_data='add_lesson_close')
    ikb_continue_add_lesson_button = InlineKeyboardButton(text='Продолжить', callback_data='add_lesson_continue')

    ikb_add_lesson\
        .add(ikb_add_lesson_button_week_day, ikb_add_lesson_button_lesson_time)\
        .add(ikb_close_add_lesson_button)\
        .add(ikb_continue_add_lesson_button)

    return ikb_add_lesson


async def select_class_student_keyboard():
    ikb_select_class_student = InlineKeyboardMarkup(row_width=4)
    for i in range(1, 12):
        ikb_class_button = InlineKeyboardButton(text=f'{i}', callback_data=f'select_class_student_{i}')
        ikb_select_class_student.insert(ikb_class_button)

    ikb_add_student_close = InlineKeyboardButton(text='Отмена', callback_data='close_option')
    ikb_select_class_student.add(ikb_add_student_close)
    return ikb_select_class_student


async def select_class_student_by_change_keyboard():
    ikb_select_class_student = InlineKeyboardMarkup(row_width=4)
    for i in range(1, 12):
        ikb_class_button = InlineKeyboardButton(text=f'{i}', callback_data=f'select_class_student_change_{i}')
        ikb_select_class_student.insert(ikb_class_button)

    ikb_change_student_close = InlineKeyboardButton(text='Отмена', callback_data='change_student_info_close_option')
    ikb_select_class_student.add(ikb_change_student_close)
    return ikb_select_class_student


async def select_week_day_for_lesson():
    ikb_select_week_day = InlineKeyboardMarkup(row_width=7)

    ikb_select_week_day_button_first = InlineKeyboardButton(text='ПН', callback_data='add_week_day_first')
    ikb_select_week_day_button_second = InlineKeyboardButton(text='ВТ', callback_data='add_week_day_second')
    ikb_select_week_day_button_third = InlineKeyboardButton(text='СР', callback_data='add_week_day_third')
    ikb_select_week_day_button_fourth = InlineKeyboardButton(text='ЧТ', callback_data='add_week_day_fourth')
    ikb_select_week_day_button_fifth = InlineKeyboardButton(text='ПТ', callback_data='add_week_day_fifth')
    ikb_select_week_day_button_sixth = InlineKeyboardButton(text='СБ', callback_data='add_week_day_sixth')
    ikb_select_week_day_button_seventh = InlineKeyboardButton(text='ВС', callback_data='add_week_day_seventh')

    ikb_select_week_day_button_close = InlineKeyboardButton(text='Отмена', callback_data='add_lesson_close_option')
    ikb_select_week_day.add(ikb_select_week_day_button_first, ikb_select_week_day_button_second, ikb_select_week_day_button_third,
                               ikb_select_week_day_button_fourth, ikb_select_week_day_button_fifth, ikb_select_week_day_button_sixth, ikb_select_week_day_button_seventh)

    ikb_select_week_day.add(ikb_select_week_day_button_close)

    return ikb_select_week_day


ikb_confirm_add_student = InlineKeyboardMarkup(row_width=1)

ikb_confirm_add_student_accept = InlineKeyboardButton(text='✅ Верно', callback_data='confirm_add_student_accept')
ikb_confirm_add_student_cancel = InlineKeyboardButton(text='❌ Отмена', callback_data='confirm_add_student_cancel')

ikb_confirm_add_student.add(ikb_confirm_add_student_accept).add(ikb_confirm_add_student_cancel)




async def ikb_manage_student_keyboard(student_id):
    ikb_manage_student = InlineKeyboardMarkup()

    ikb_manage_student_button_add_lesson = InlineKeyboardButton(text='Добавить урок', callback_data=f'add_new_lesson_{student_id}')
    ikb_manage_student_button_change_info = InlineKeyboardButton(text='Изменить информацию', callback_data=f'change_student_info_{student_id}')
    ikb_manage_student_button_lessons_list = InlineKeyboardButton(text='Расписание уроков', callback_data=f'schedule_current_student_{student_id}')
    ikb_manage_student_button_back = InlineKeyboardButton(text='⬅️ Назад', callback_data=f'manage_student_back_{student_id}')

    ikb_manage_student.add(ikb_manage_student_button_add_lesson).add(ikb_manage_student_button_change_info).add(ikb_manage_student_button_lessons_list).add(ikb_manage_student_button_back)

    return ikb_manage_student


async def ikb_back_button(student_id):
    ikb_back = InlineKeyboardMarkup(row_width=1)

    ikb_button_back = InlineKeyboardButton(text='⬅️ Назад', callback_data=f'manage_student_back_{student_id}')

    ikb_back.add(ikb_button_back)

    return ikb_back


async def change_student_info(student_id):
    change_student_info_ikb = InlineKeyboardMarkup(row_width=3)

    change_student_info_id = InlineKeyboardButton(text='ID', callback_data=f'student_info_change_id_{student_id}')
    change_student_info_name = InlineKeyboardButton(text='Имя', callback_data=f'student_info_change_name_{student_id}')
    change_student_info_subject = InlineKeyboardButton(text='Предмет', callback_data=f'student_info_change_subject_{student_id}')
    change_student_info_class = InlineKeyboardButton(text='Класс', callback_data=f'student_info_change_class_{student_id}')
    change_student_info_purpose = InlineKeyboardButton(text='Цель', callback_data=f'student_info_change_purpose_{student_id}')
    change_student_info_price = InlineKeyboardButton(text='Цена', callback_data=f'student_info_change_price_{student_id}')
    change_student_info_transfer = InlineKeyboardButton(text='Трансфер', callback_data=f'student_info_change_transfer_{student_id}')
    change_student_info_phone = InlineKeyboardButton(text='Телефон', callback_data=f'student_info_change_phone_{student_id}')
    change_student_info_platform = InlineKeyboardButton(text='Платформа', callback_data=f'student_info_change_platform_{student_id}')
    change_student_info_nick = InlineKeyboardButton(text='Ник', callback_data=f'student_info_change_nick_{student_id}')
    change_student_info_timezone = InlineKeyboardButton(text='ЧП', callback_data=f'student_info_change_timezone_{student_id}')
    change_student_info_back = InlineKeyboardButton(text='⬅️ Назад', callback_data=f'manage_student_back_{student_id}')

    change_student_info_ikb.add(change_student_info_id, change_student_info_name, change_student_info_subject, change_student_info_class, change_student_info_purpose, change_student_info_price, change_student_info_transfer, change_student_info_phone, change_student_info_platform, change_student_info_nick, change_student_info_timezone)
    change_student_info_ikb.add(change_student_info_back)
    return change_student_info_ikb


