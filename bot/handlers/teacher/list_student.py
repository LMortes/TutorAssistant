from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.keyboards import inline as ikb
from bot.loader import dp, bot
from bot.utils.mysql import db
from bot.utils.other.generate_info_student import generate_info_student
from bot.utils.other.parse_registration_date import parse_registration_date

@dp.message_handler(Text('👨‍🎓Список учеников'))
async def show_list_students(message: types.Message):
    students_info = await db.get_students(message.from_user.id)
    if students_info != False:
        info_message = 'Список учеников:'

        await message.answer(info_message, reply_markup=await ikb.ikb_list_students(students_info))
    else:
        await message.answer('Ученики отсутствуют.')


@dp.callback_query_handler(lambda callback: callback.data.startswith('list_students_'))
async def list_student_callback(callback: types.CallbackQuery):
    student_id = callback.data[14:]
    info_message = await generate_info_student(student_id)

    await bot.edit_message_text(info_message, callback.message.chat.id, callback.message.message_id, reply_markup=await ikb.ikb_student_info(student_id))


@dp.callback_query_handler(lambda callback: callback.data.startswith('student_info_back'))
async def back_to_list_students_callback(callback: types.CallbackQuery):
    students_info = await db.get_students(callback.from_user.id)
    info_message = 'Список учеников:'

    await bot.edit_message_text(info_message, callback.message.chat.id, callback.message.message_id, reply_markup=await ikb.ikb_list_students(students_info))