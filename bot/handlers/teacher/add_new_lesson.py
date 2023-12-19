import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.bin.russian_weekdays import russian_weekday
from bot.keyboards import inline as ikb
from bot.loader import dp, bot
from bot.utils.mysql import db
from bot.utils.other.generate_schedule_current_student import generate_schedule_current_student
from bot.utils.other.parse_registration_date import parse_registration_date
from bot.utils.states.add_lesson_state import AddLesson


async def get_info_lesson(state):
    data = await state.get_data()
    lesson_info = {
        'week_day': data.get('week_day'),
        'lesson_time': data.get('lesson_time'),
    }
    return lesson_info

async def generate_info_student_message(lesson_info, student_id=None):
    schedule_current_student = ''
    if student_id is not None:
        lesson_dates = await db.get_lesson_dates_current_student(student_id)

        if lesson_dates != False:
            schedule_current_student = await generate_schedule_current_student(lesson_dates)  # Получим уже имеющееся расписание ученика

    current_schedule_message = ''
    if len(schedule_current_student) != 0:
        current_schedule_message = f'У этого ученика уже есть раснисание:\n{schedule_current_student}'


    pre_message = '⚙️ Ты вошел в режим добавления урока для ученика' \
                  '\nИспользуй кнопки чтобы добавлять информацию об уроке' \
                  '\n\n🔴 Красным кружком помечены поля обязательные для заполнения, остальные по желанию' \
                  '\n\n☑️ После заполнения, нажми "Продолжить" и расписание автоматически сгенерируется до конца года на заполненный день\n\n'\
                   f'{current_schedule_message}'

    info_message = (f'{pre_message}Информация об уроке:\n\n'
                    f'📅 День недели: {"-" if lesson_info["week_day"] is None else lesson_info["week_day"]}\n'
                    f'🕒 Время (мск): {"-" if lesson_info["lesson_time"] is None else lesson_info["lesson_time"]}')
    return info_message



@dp.callback_query_handler(lambda callback: callback.data.startswith('add_new_lesson_'))
async def add_new_lesson_to_student_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    student_id = callback.data[15:]
    teacher_id = callback.from_user.id

    await state.set_state(AddLesson.add_lesson_state)
    await state.update_data(student_id=student_id, teacher_id=teacher_id, week_day=None, lesson_time=None)
    lesson_info = await get_info_lesson(state)
    info_message = await generate_info_student_message(lesson_info, student_id)
    main_message = await callback.message.answer(f'{info_message}',
                                        reply_markup=await ikb.generate_keyboard_add_lesson(lesson_info))
    main_message_id = main_message.message_id
    await state.update_data(main_message_id=main_message_id)



@dp.callback_query_handler(lambda callback: callback.data == 'add_lesson_close_option', state=['*'])
async def close_option_add_lesson_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(AddLesson.add_lesson_state)
    return await callback.answer('Действие отменено')



@dp.callback_query_handler(lambda callback: callback.data.startswith('add_week_day_'),
                           state=AddLesson.add_week_day)
async def add_week_day_callback(callback: types.CallbackQuery, state: FSMContext):
    week_day = callback.data[13:]
    week_day_text = ''
    if week_day == 'first':
        week_day_text = 'Понедельник'
        week_day = 0
    elif week_day == 'second':
        week_day_text = 'Вторник'
        week_day = 1
    elif week_day == 'third':
        week_day_text = 'Среда'
        week_day = 2
    elif week_day == 'fourth':
        week_day_text = 'Четверг'
        week_day = 3
    elif week_day == 'fifth':
        week_day_text = 'Пятница'
        week_day = 4
    elif week_day == 'sixth':
        week_day_text = 'Суббота'
        week_day = 5
    elif week_day == 'seventh':
        week_day_text = 'Воскресенье'
        week_day = 6


    await state.update_data(week_day=week_day_text, week_day_info=week_day)

    # Добываем ид предыдущих сообщений для последующего удаления
    main_message_id = (await state.get_data()).get('main_message_id')
    callback_message_id = (await state.get_data()).get('callback_message_id')
    lesson_info = await get_info_lesson(state)
    info_message = await generate_info_student_message(lesson_info)
    await bot.delete_message(callback.message.chat.id, callback_message_id)
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=main_message_id, text=f'{info_message}', \
                                reply_markup=await ikb.generate_keyboard_add_lesson(lesson_info))
    await state.set_state(AddLesson.add_lesson_state)  # Устанавливаем состояние редактирования информации урока


@dp.message_handler(state=AddLesson.add_lesson_time)
async def add_lesson_time_handler(message: types.Message, state: FSMContext):
    time_pattern = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')

    if time_pattern.match(message.text):
        lesson_hour = (message.text.split(':'))[0]
        lesson_minute = (message.text.split(':'))[1]

        lesson_time = f'{lesson_hour}:{lesson_minute}'
        await state.update_data(lesson_time=lesson_time)

        # Добываем ид предыдущих сообщений для последующего удаления
        main_message_id = (await state.get_data()).get('main_message_id')
        callback_message_id = (await state.get_data()).get('callback_message_id')
        lesson_info = await get_info_lesson(state)
        info_message = await generate_info_student_message(lesson_info)
        await bot.delete_message(message.chat.id, callback_message_id)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=main_message_id,
                                    text=f'{info_message}',
                                    reply_markup=await ikb.generate_keyboard_add_lesson(lesson_info))
        await state.set_state(AddLesson.add_lesson_state)  # Устанавливаем состояние редактирования информации урока
    else:
        return await message.answer('❗️ Неверный ввод времени. Попробуйте заного соблюдая форму ввода.')



@dp.callback_query_handler(lambda callback: callback.data.startswith('add_lesson_'),
                           state=AddLesson.add_lesson_state)
async def add_lesson_callback(callback: types.CallbackQuery, state: FSMContext):
    message_callback = callback.data[11:]

    if message_callback == 'week_day':
        await state.set_state(AddLesson.add_week_day)
        callback_message = await callback.message.answer(
            'Выбери день недели в который будет урок с учеником:',
            reply_markup=await ikb.select_week_day_for_lesson())
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'lesson_time':
        await state.set_state(AddLesson.add_lesson_time)
        callback_message = await callback.message.answer(
            '⏳ Напиши время в которое будет урок с учеником\n\n'
            'Например:\n'
            '02:35\n'
            '16:00\n'
            '00:20')
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'close':
        await callback.message.delete()
        await callback.answer('Действие отменено')
        return await state.finish()
    elif message_callback == 'continue':
        lesson_info = await get_info_lesson(state)
        if ((lesson_info["week_day"] is not None) and (lesson_info["lesson_time"] is not None)):
            wait_message = await callback.message.answer('⏳ Процедурная генерация расписания... Пожалуйста подождите.')
            data = await state.get_data()
            await db.generate_lessons_for_weekday(data.get("teacher_id"), data.get("student_id"),
                                                  data.get("week_day_info"), data.get("lesson_time"))
            await callback.message.delete()
            await bot.delete_message(callback.message.chat.id, wait_message.message_id)
            await callback.message.answer(
                f'✅ Расписание на {data.get("week_day")} в {data.get("lesson_time")} успешно сгенерировано.')
            await state.reset_data()
            await state.finish()
            return await callback.answer()
        else:
            return await callback.answer('❌ Некоторые из обязательных полей не были заполнены.')


