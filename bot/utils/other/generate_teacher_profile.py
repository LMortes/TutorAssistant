from bot.utils.mysql import db
from bot.utils.other.parse_registration_date import parse_registration_date



async def generate_teacher_profile(teacher_info):
    profile_text = ''
    id = teacher_info[0]
    user_id = teacher_info[1]
    name = teacher_info[2]
    subject = teacher_info[3]
    registration_date = teacher_info[4]
    profile_text += f'{"<b>Архивный</b> " if teacher_info[5] == 1 else ""}'
    # ФИО[id]
    # Предмет
    # Количество учеников
    # Месячный доход
    # Проведенных уроков
    # Отмененных уроков
    # Количество учеников за все время
    # Дата регистрации
    count_student = await db.get_count_active_students_for_teacher(id)
    count_students_all = await db.get_count_all_students_for_teacher(id)
    mount_price = await db.get_mounth_price_for_teacher(id)

    # Статусы уроков
    # 0 - Еще не проведен
    # 1 - Проведен
    # 2 - Отменен
    # 3 - Перенесен

    parse_date_info = await parse_registration_date(registration_date)
    success_lessons = await db.get_count_lessons_for_teacher(id, status=2)
    canceled_lessons = await db.get_count_lessons_for_teacher(id, status=4)
    redate_lessons = await db.get_count_lessons_for_teacher(id, status=3)
    profile_text += f'🟣 {name}[{user_id}]\n' \
                    f'✍️ Предмет: {subject}\n' \
                    f'👨‍🎓 Количество учеников: {"0" if not count_student else count_student}\n' \
                    f'💰 Месячный доход: {"0" if not mount_price else mount_price } ₽\n'\
                    f'✅ Проведенных уроков: {success_lessons}\n'\
                    f'❌ Отмененных уроков: {canceled_lessons}\n'\
                    f'♻️ Перенесенных уроков: {redate_lessons}\n'\
                    f'♾ Количество учеников за всё время: {"0" if not count_students_all else count_students_all}\n'\
                    f'📅 Дата регистрации: {parse_date_info["day"]} {parse_date_info["month"]} {parse_date_info["year"]} года в {parse_date_info["hour"]}:{parse_date_info["minute"]}\n'
    return profile_text
