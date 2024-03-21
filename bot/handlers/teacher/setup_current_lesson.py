import datetime

from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.bin.russian_weekdays import russian_weekday
from bot.keyboards import inline as ikb
from bot.loader import dp, bot
from bot.utils.mysql import db


################ Тестовая функция. Удалить!
@dp.message_handler(commands=['lesson'])
async def test_current_lesson_handler(message: types.Message):
    lesson_info = (493, 1000, datetime.datetime(2024, 3, 14, 22, 59), 812267139, 'Свиридов Евгений Сергеевич', 4115, 'Катя', 'Математика', 8, 'Успеваемость', 'Discord', 'karga')

    lesson_info_message = ''

    # Форматируем вывод ника на платформе, если поступило не None
    platform_nick = " - " + lesson_info[11]
    platform_nick_message = f'{"" if lesson_info[11] == None else platform_nick}'

    lesson_info_message = f'Начался урок\n\nУченик: {lesson_info[6]}\nКласс: {lesson_info[8]}\nПредмет: {lesson_info[7]}\nПлатформа: {lesson_info[10]}{platform_nick_message}\nЦель занятий: {lesson_info[9]}\nСтоимость: {lesson_info[1]}'
    await bot.send_message(lesson_info[3], text=lesson_info_message, reply_markup=await ikb.setup_current_lesson(lesson_info[0]))

@dp.callback_query_handler(lambda callback: callback.data.startswith('setup_current_lesson_'))
async def setup_current_lesson_callback(callback: types.CallbackQuery):
    message_callback = callback.data[21:]
    status_lesson = 1
    if message_callback.startswith('success'):
        lesson_id = (message_callback.split(':')[0])[8:]
        is_payed_lesson = message_callback.split(':')[1] == 'True' # Преобразуем строку в булево значение
        
        status_lesson = 2 # Устанавливаем новый статус уроку "2 - Проведен"
        try:
            await db.change_lesson_status(lesson_id=lesson_id, new_status=status_lesson)
        except Exception as e:
            print(e)
        
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.edit_text(text=f'✅ {callback.message.text} {"✔️" if is_payed_lesson else "✖️"}')
        await callback.answer()
    elif message_callback.startswith('denied'):
        lesson_id = (message_callback.split(':')[0])[7:]
        is_payed_lesson = message_callback.split(':')[1] == 'True' # Преобразуем строку в булево значение
        
        status_lesson = 4 # Устанавливаем новый статус уроку "4 - Отменен"
        try:
            await db.change_lesson_status(lesson_id=lesson_id, new_status=status_lesson)
        except Exception as e:
            print(e)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.edit_text(text=f'❌ {callback.message.text} {"✔️" if is_payed_lesson else "✖️"}')
        await callback.answer()
    elif message_callback.startswith('payed'):
        await callback.answer()
        lesson_id = (message_callback.split(':')[0])[6:]
        is_payed_lesson = message_callback.split(':')[1] != 'True' # Инвертирует значение переменной is_payed_lesson на противоположное 
        await callback.message.edit_reply_markup(reply_markup=await ikb.setup_current_lesson(lesson_id=lesson_id, is_payed_lesson=is_payed_lesson))
    elif message_callback.startswith('change_date'):
        await callback.answer('В разработке')
