from aiogram import types
from aiogram.dispatcher.filters import Text
from bot.keyboards import inline as ikb
from bot.loader import dp, bot
from bot.utils.mysql import db
from bot.utils.other.generate_teacher_profile import generate_teacher_profile
from bot.utils.other.parse_registration_date import parse_registration_date

@dp.message_handler(Text('🗓 Список репетиторов'))
async def show_list_teachers(message: types.Message):
    teachers_info = await db.get_teachers()
    info_message = 'Список репетиторов:'

    await message.answer(info_message, reply_markup=await ikb.ikb_list_teachers(teachers_info))


@dp.callback_query_handler(lambda callback: callback.data.startswith('list_teachers_'))
async def list_teacher_callback(callback: types.CallbackQuery):
    teacher_id = callback.data[14:]
    teacher_info = await db.get_teacher_info_by_id(teacher_id)
    profile_text = await generate_teacher_profile(teacher_info)
    # await callback.message.answer(profile_text)


    # parse_date_info = await parse_registration_date(teacher_info[4])

    # info_message = f'ℹ️ Информация о репетиторе\n\n' \
    #                f'🆔 ID: {teacher_info[1]}\n' \
    #                f'🟣 ФИО: {teacher_info[2]}\n' \
    #                f'✍️ Преподаваемый предмет: {teacher_info[3]}\n' \
    #                f'📅 Дата регистрации: {parse_date_info["day"]} {parse_date_info["month"]} {parse_date_info["year"]} года в {parse_date_info["hour"]}:{parse_date_info["minute"]}'

    await bot.edit_message_text(profile_text, callback.message.chat.id, callback.message.message_id, reply_markup=await ikb.ikb_teacher_info(teacher_id))


@dp.callback_query_handler(lambda callback: callback.data.startswith('teacher_info_back'))
async def back_to_list_teachers_callback(callback: types.CallbackQuery):
    teachers_info = await db.get_teachers()
    info_message = 'Список репетиторов:'

    await bot.edit_message_text(info_message, callback.message.chat.id, callback.message.message_id, reply_markup=await ikb.ikb_list_teachers(teachers_info))