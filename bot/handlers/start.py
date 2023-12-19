import os
from aiogram import types
from bot.filters import IsNotAdminUser
from bot.keyboards import inline as ikb
from bot.keyboards import default as kb
from bot.loader import bot, dp
from bot.utils.mysql import db



@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_exists = await db.user_exists(user_id)
    if user_exists:
        teacher_info = await db.get_teacher_info(user_id)
        if not teacher_info:
            student_info = await db.get_student_info(user_id)
            return await message.answer(f'Вы авторизованы как ученик: {student_info["name"]}', reply_markup=kb.ikb_menu_student)
        else:
            return await message.answer(f'Вы авторизованы как репетитор: {teacher_info["name"]}', reply_markup=await kb.ikb_menu_teacher(message.from_user.id))
    else:
        await message.answer('Авторизуйся в боте:', reply_markup=ikb.ikb_auth)


@dp.callback_query_handler(lambda callback: callback.data.startswith('auth_'))
async def auth_callback(callback: types.CallbackQuery):
    callback_message = callback.data[5:]
    user_id = callback.from_user.id
    if callback_message == 'teacher':
        teacher_info = await db.get_teacher_info(user_id)
        if not teacher_info:
            return await callback.answer('❌ Отказано в доступе. Ты не найден в базе данных репетиторов.', show_alert=True)
        else:
            await callback.message.delete()
            return await callback.message.answer(f'Вы авторизованы как репетитор: {teacher_info["name"]}', reply_markup=await kb.ikb_menu_teacher(callback.from_user.id))
    elif callback_message == 'student':
        student_info = await db.get_student_info(user_id)
        if not student_info:
            return await callback.answer('❌ Тебя еще нет в базе данных учеников. Обратись к своему репетитору', show_alert=True)
        else:
            await callback.message.delete()
            return await callback.message.answer(f'Вы авторизованы как ученик: {student_info["name"]}', reply_markup=kb.ikb_menu_student)




@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.answer('Помощь')
