import datetime

from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.bin.russian_weekdays import russian_weekday
from bot.keyboards import inline as ikb
from bot.loader import dp, bot
from bot.utils.mysql import db
from bot.utils.other.parse_registration_date import parse_registration_date


@dp.message_handler(Text("🗓 Раписание на сегодня"))
async def schedule_today_handler(message: types.Message):
    teacher_id = message.from_user.id

    current_date = datetime.datetime.now().date()

    # Получение текущего дня недели в виде названия
    weekday_name = russian_weekday[current_date.strftime("%A")]  # "%A" форматирует дату как название дня недели

    lessons_info = await db.get_lessons_current_date(teacher_id, current_date)
    # output ((9876, 'ergverg', datetime.datetime(2023, 12, 8, 18, 0), 12341234), (9876, 'ergverg', datetime.datetime(2023, 12, 8, 20, 0), 12341234))
    if lessons_info != False:
        schedule_message = f'📆 <b>Расписание на сегодня ( {weekday_name} )</b>\n\n'
        schedule_lesson = ''
        count_rubles = 0
        for lesson in lessons_info:
            schedule_lesson += f'{lesson[2].strftime("%H:%M")}     {lesson[1]}    {lesson[3]} ₽\n'
            count_rubles += int(lesson[3])

        await message.answer(f'{schedule_message}{schedule_lesson}\n💵 <b>Стоимость дня:</b> {count_rubles} ₽')
    else:
        await message.answer('🎉 Сегодня уроков нет.')