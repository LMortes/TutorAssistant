import datetime
import locale

from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.bin.russian_weekdays import russian_weekday
from bot.keyboards import inline as ikb
from bot.loader import dp, bot
from bot.utils.mysql import db
from bot.utils.other.generate_info_student import generate_info_student
from bot.utils.other.generate_schedule_current_student import generate_schedule_current_student
from bot.utils.other.parse_registration_date import parse_registration_date





@dp.callback_query_handler(lambda callback: callback.data.startswith('manage_student_back_'))
async def manage_student_callback_back(callback: types.CallbackQuery):
    try:
        student_id = callback.data[20:]
        info_message = await generate_info_student(student_id)

        await bot.edit_message_text(info_message, callback.message.chat.id, callback.message.message_id,
                                    reply_markup=await ikb.ikb_student_info(student_id))
    except:
        await callback.answer()


@dp.callback_query_handler(lambda callback: callback.data.startswith('manage_student_'))
async def manage_student_callback_handler(callback: types.CallbackQuery):
    student_id = callback.data[15:]
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=await ikb.ikb_manage_student_keyboard(student_id))


@dp.callback_query_handler(lambda callback: callback.data.startswith("schedule_current_student_"))
async def get_schedule_current_student(callback: types.CallbackQuery):
    student_id = callback.data[25:]
    lesson_dates = await db.get_lesson_dates_current_student(student_id)

    if lesson_dates != False:
        schedule_info_message = await generate_schedule_current_student(lesson_dates)
        await bot.edit_message_text(schedule_info_message, callback.message.chat.id, callback.message.message_id,
                                    reply_markup=await ikb.ikb_back_button(student_id))

        return await callback.answer()
    else:
        return await callback.answer('Уроки отсутствуют.')

