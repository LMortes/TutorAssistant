from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ADMIN_ID = 812267139
async def ikb_menu_teacher(user_id):
    ikb_menu_teacher = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    ikb_menu_teacher_button_add_student = KeyboardButton(text='➕ Добавить ученика')
    ikb_menu_teacher_button_current_day = KeyboardButton('🗓 Раписание на сегодня')
    ikb_menu_teacher_button_current_week = KeyboardButton('🗓 Раписание на неделю')
    ikb_menu_teacher_button_profile = KeyboardButton('📊 Профиль')
    ikb_menu_teacher_button_list_students = KeyboardButton('👨‍🎓Список учеников')
    ikb_menu_teacher_button_statistics = KeyboardButton(text='⚙️ Настройки')
    ikb_menu_teacher_button_add_teacher = KeyboardButton(text='👨‍🏫 Добавить репетитора')
    ikb_menu_teacher_button_list_teachers = KeyboardButton(text='🗓 Список репетиторов')

    ikb_menu_teacher\
        .add(
        ikb_menu_teacher_button_add_student,
        ikb_menu_teacher_button_current_day,
        ikb_menu_teacher_button_current_week)\
        .add(
        ikb_menu_teacher_button_list_students,
        ikb_menu_teacher_button_profile,
        ikb_menu_teacher_button_statistics)

    if user_id == ADMIN_ID:
        ikb_menu_teacher.add(ikb_menu_teacher_button_add_teacher, ikb_menu_teacher_button_list_teachers)

    return ikb_menu_teacher




ikb_menu_student = ReplyKeyboardMarkup(row_width=3)

ikb_menu_student_button_dev = KeyboardButton(text='В разработке')

ikb_menu_student.add(ikb_menu_student_button_dev)