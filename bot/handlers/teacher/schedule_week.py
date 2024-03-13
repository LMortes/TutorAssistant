import datetime
from datetime import timedelta
from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.bin.russian_weekdays import russian_weekday
from bot.keyboards import inline as ikb
from bot.loader import dp, bot
from bot.utils.mysql import db


@dp.message_handler(Text("🗓 Раписание на неделю"))
async def schedule_today_and_next_six_days_handler(message: types.Message):
    teacher_id = message.from_user.id

    current_date = datetime.datetime.now().date()

    weekdays = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'}

    for i in range(7):
        target_date = current_date + timedelta(days=i)
        weekday_name = russian_weekday[target_date.strftime("%A")]

        lessons_info = await db.get_lessons_current_date(teacher_id, target_date)

        if lessons_info:
            schedule_message = f'📆 <b>Расписание на {weekday_name} ({target_date.strftime("%d.%m.%y")})</b>\n\n'
            schedule_lesson = ''
            count_rubles = 0

            # for lesson in lessons_info:
            #     schedule_lesson += f'{lesson[2].strftime("%H:%M")}     {lesson[1]}    {lesson[3]} ₽\n'
            #     count_rubles += int(lesson[3])
            
            for lesson in lessons_info:
                if lesson[4] == 3:
                    schedule_lesson += f'<blockquote>{lesson[2].strftime("%H:%M")}     {lesson[1]}    {lesson[3]} ₽</blockquote>\n'
                elif lesson[4] == 4:
                    schedule_lesson += f'<s>{lesson[2].strftime("%H:%M")}     {lesson[1]}    {lesson[3]} ₽</s>\n'
                    count_rubles -= int(lesson[3])
                else:
                    schedule_lesson += f'{lesson[2].strftime("%H:%M")}     {lesson[1]}    {lesson[3]} ₽\n'
                count_rubles += int(lesson[3])
            
            await message.answer(f'{schedule_message}{schedule_lesson}\n💵 <b>Стоимость дня:</b> {count_rubles} ₽')
        else:
            await message.answer(f'🎉 На {weekday_name} ({target_date.strftime("%d.%m.%y")}) уроков нет.')