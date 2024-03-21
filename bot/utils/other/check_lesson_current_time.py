import asyncio
import datetime
from aiogram.utils.exceptions import RetryAfter
from bot.utils.mysql import db
from bot.keyboards import inline as ikb

async def send_message_to_teacher_at_current_time(bot, lesson_info):
    lesson_info_message = ''

    # Форматируем вывод ника на платформе, если поступило не None
    platform_nick = " - " + lesson_info[11]
    platform_nick_message = f'{"" if lesson_info[11] == None else platform_nick}'

    lesson_info_message = f'Начался урок\n\nУченик: {lesson_info[6]}\nКласс: {lesson_info[8]}\nПредмет: {lesson_info[7]}\nПлатформа: {lesson_info[10]}{platform_nick_message}\nЦель занятий: {lesson_info[9]}\nСтоимость: {lesson_info[1]}'

    try:  # Пробуем отправить сообщение репетитору
        await db.change_lesson_status(lesson_id=lesson_info[0], new_status=1) # При поступлении сообщения репетитору, статус урока сменяется на "1 - Идет в данный момент"
        await bot.send_message(lesson_info[3], text=lesson_info_message, reply_markup=await ikb.setup_current_lesson(lesson_info[0]))
    except RetryAfter as e:  # обрабатываем ошибку слишком частой отправки
        await asyncio.sleep(e.timeout)
        return await send_message_to_teacher_at_current_time(lesson_info)
    except Exception as e:
        print(e)
        return False
    else:  # возвращаем True, если прошло успешно
        return True


async def check_lesson_current_time(bot):
    await asyncio.sleep(1)
    # start_time = datetime.datetime.now()
    current_datetime = datetime.datetime.now()
    formatted_current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:00')
    lessons_info = await db.get_lessons_current_date_and_time(formatted_current_datetime)

    # (576, 1000, datetime.datetime(2024, 3, 14, 22, 59), 812267139, 'Свиридов Евгений Сергеевич', 4115, 'Катя', 'Математика', 8, 'Успеваемость', 'Discord', 'karga')
    # Формат вывода:
    # (l_id, l_price, l_date, t_tg_id, t_name, s_tg_id, s_name, s_subject, s_class, s_purpose, s_platform, s_p_nick)

    if lessons_info != False:
        try:
            for lesson_info in lessons_info:
                if await send_message_to_teacher_at_current_time(bot, lesson_info):
                    # В будущем для логирования
                    # successful_count += 1
                    pass
                await asyncio.sleep(0.05)
                
        finally:
            pass
            # logger.info(f'Сообщения репетиторам разосланы., {successful_count} репетиторов получили сообщения.')
    else:
        # Для логирования
        pass
        # print('Уроков на данный момент нет.')
    # end_time = datetime.datetime.now()
    # execution_time = end_time - start_time
    # print("Время выполнения скрипта:", execution_time)
    # print('-----------------------------------')


async def run_periodic_check_lesson_current_time(bot):
    await asyncio.gather(
        check_lesson_current_time(bot)
    )