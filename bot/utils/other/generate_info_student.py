from bot.utils.mysql import db
from bot.utils.other.parse_registration_date import parse_registration_date


async def generate_info_student(student_id):
    student_info = await db.get_student_info_by_id(student_id)
    parse_date_info = await parse_registration_date(student_info[4])

    info_message = f'ℹ️ Информация об ученике\n\n' \
                   f'🆔 ID: {student_info[1]}\n' \
                   f'🟣 ФИО: {student_info[2]}\n' \
                   f'📖 Предмет: {student_info[3] if student_info[3] != "None" else "-"}\n' \
                   f'🔢 Класс: {student_info[5] if student_info[5] != "None" else "-"}\n' \
                   f'⚠️ Уклон: {student_info[6] if student_info[6] != "None" else "-"}\n' \
                   f'💰 Цена: {student_info[7] if student_info[7] != "None" else "-"}\n' \
                   f'♻️ Трансфер: {student_info[8] if student_info[8] != "None" else "-"}\n' \
                   f'📞 Номер телефона: {student_info[9] if student_info[9] != "None" else "-"}\n' \
                   f'💬 Платформа: {student_info[10] if student_info[10] != "None" else "-"}\n' \
                   f'🏷 Ник на платформе: {student_info[11] if student_info[11] != "None" else "-"}\n' \
                   f'🕒 Часовой пояс: {student_info[12] if student_info[12] != "None" else "-"}\n' \
                   f'👨‍🏫 Преподаватель: {student_info[16]}[{student_info[15]}]\n' \
                   f'📅 Дата регистрации: {parse_date_info["day"]} {parse_date_info["month"]} {parse_date_info["year"]} года в {parse_date_info["hour"]}:{parse_date_info["minute"]}'
    return info_message