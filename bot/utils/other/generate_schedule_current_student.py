from bot.bin.russian_weekdays import russian_weekday


async def generate_schedule_current_student(lesson_dates):
    schedule = {}
    for row in lesson_dates:
        lesson_date = row[0]  # Получаем дату урока
        weekday = lesson_date.strftime("%A")  # Получаем название дня недели
        time = lesson_date.strftime("%H:%M")  # Получаем время урока
        if weekday not in schedule:
            schedule[weekday] = set()  # Используем множество для хранения времени уроков
        schedule[weekday].add(time)
    print(len(schedule))
    schedule_info_message = '📆 <b>Расписание:</b>\n\n'
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in sorted(schedule.keys(), key=lambda x: order.index(x)):
        sorted_times = sorted(schedule[day])
        schedule_info_message += f"{russian_weekday[day]}\n {' '.join(sorted_times)}\n\n"

    return schedule_info_message
