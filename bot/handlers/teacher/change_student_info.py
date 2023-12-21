from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.loader import dp, bot
from bot.keyboards import inline as ikb
from bot.utils.mysql import db
from bot.utils.other.generate_info_student import generate_info_student
from bot.utils.states.change_student_info_state import ChangeStudentInfo



async def delete_message_and_successful_change_info(message, state):
    callback_message_id = (await state.get_data()).get('callback_message_id')
    await message.delete()
    data = await state.get_data()
    info_message = await generate_info_student(data.get("student_id"))

    await bot.edit_message_text(info_message, message.chat.id, data.get("main_message_id"),
                                reply_markup=await ikb.ikb_student_info(data.get("student_id")))
    try:
        await bot.delete_message(message.chat.id, callback_message_id)
    except:
        pass
    await message.answer('✅ Информация успешно изменена!')
    await state.finish()


@dp.callback_query_handler(lambda callback: callback.data == 'change_student_info_close_option', state=['*'])
async def close_option_change_info_student_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.finish()
    return await callback.answer('Действие отменено')


@dp.callback_query_handler(lambda callback: callback.data.startswith("change_student_info_"))
async def change_student_info_callback(callback: types.CallbackQuery):
    student_id = callback.data[20:]

    message_text = callback.message.text
    changed_message_text = f'{message_text}\n\nЧто меняем?'

    await bot.edit_message_text(changed_message_text, callback.message.chat.id, callback.message.message_id, reply_markup=await ikb.change_student_info(student_id))



@dp.message_handler(state=ChangeStudentInfo.get_student_id)
async def get_new_student_id_handler(message: types.Message, state: FSMContext):
    new_student_id = message.text

    # Обработка ошибок
    try:
        new_student_id = int(new_student_id)
    except:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. ID должен состоять только из цифр.')
    if int(new_student_id) < 0:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. ID пользователя не может быть отрицательным.')

    student_id_exists = await db.get_student_info(new_student_id)
    if student_id_exists != False:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. Ученик с таким ID уже есть в базе данных.')

    data = await state.get_data()
    await db.change_student_id(data.get("student_id"), new_student_id)
    await state.update_data(student_id=new_student_id)
    return await delete_message_and_successful_change_info(message, state)



@dp.message_handler(state=ChangeStudentInfo.get_student_name)
async def get_new_student_name_handler(message: types.Message, state: FSMContext):
    new_student_name = message.text

    data = await state.get_data()
    await db.change_student_name(data.get("student_id"), new_student_name)

    return await delete_message_and_successful_change_info(message, state)



@dp.message_handler(state=ChangeStudentInfo.get_student_subject)
async def get_new_student_subject_handler(message: types.Message, state: FSMContext):
    new_subject = message.text

    data = await state.get_data()
    await db.change_student_subject(data.get("student_id"), new_subject)

    return await delete_message_and_successful_change_info(message, state)


@dp.callback_query_handler(lambda callback: callback.data.startswith('select_class_student_change_'), state=ChangeStudentInfo.get_student_class)
async def get_new_class_student_callback(callback: types.CallbackQuery, state: FSMContext):
    new_class_student = callback.data[28:]

    data = await state.get_data()
    await db.change_student_class(data.get("student_id"), new_class_student)

    return await delete_message_and_successful_change_info(callback.message, state)


@dp.message_handler(state=ChangeStudentInfo.get_student_purpose)
async def get_new_student_purpose_handler(message: types.Message, state: FSMContext):
    new_purpose = message.text

    data = await state.get_data()
    await db.change_student_purpose(data.get("student_id"), new_purpose)

    return await delete_message_and_successful_change_info(message, state)



@dp.message_handler(state=ChangeStudentInfo.get_student_price)
async def get_new_student_price_handler(message: types.Message, state: FSMContext):
    new_price = message.text

    try:
        new_price = int(new_price)
    except:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. Ценник должен быть целым числом.')
    if int(new_price) < 0:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. Ценник не может быть отрицательным.')

    data = await state.get_data()
    await db.change_student_price(data.get("student_id"), new_price)

    return await delete_message_and_successful_change_info(message, state)


@dp.message_handler(state=ChangeStudentInfo.get_student_transfer)
async def get_new_student_transfer_handler(message: types.Message, state: FSMContext):
    new_transfer = message.text

    data = await state.get_data()
    await db.change_student_transfer(data.get("student_id"), new_transfer)

    return await delete_message_and_successful_change_info(message, state)



@dp.message_handler(state=ChangeStudentInfo.get_student_phone)
async def get_new_student_phone_handler(message: types.Message, state: FSMContext):
    new_phone = message.text

    data = await state.get_data()
    await db.change_student_phone(data.get("student_id"), new_phone)

    return await delete_message_and_successful_change_info(message, state)



@dp.message_handler(state=ChangeStudentInfo.get_student_platform)
async def get_new_student_platform_handler(message: types.Message, state: FSMContext):
    new_platform = message.text

    data = await state.get_data()
    await db.change_student_platform(data.get("student_id"), new_platform)

    return await delete_message_and_successful_change_info(message, state)



@dp.message_handler(state=ChangeStudentInfo.get_student_nick)
async def get_new_student_nick_handler(message: types.Message, state: FSMContext):
    new_nick = message.text

    data = await state.get_data()
    await db.change_student_nick(data.get("student_id"), new_nick)

    return await delete_message_and_successful_change_info(message, state)



@dp.message_handler(state=ChangeStudentInfo.get_student_timezone)
async def get_new_student_timezone_handler(message: types.Message, state: FSMContext):
    new_timezone = message.text

    if not new_timezone.startswith('+'):
        await message.delete()
        return await message.answer(
            '❗️ Неверный ввод. Отсутствует плюс перед числом, или другая синтаксическая ошибка.')

    data = await state.get_data()
    await db.change_student_timezone(data.get("student_id"), new_timezone)

    return await delete_message_and_successful_change_info(message, state)



@dp.callback_query_handler(lambda callback: callback.data.startswith("student_info_change_"))
async def student_info_change_id_callback(callback: types.CallbackQuery, state: FSMContext):
    change_parametr = callback.data[20:]
    if change_parametr.startswith('id'):
        await state.set_state(ChangeStudentInfo.get_student_id)
        callback_message = await callback.message.answer('Напиши новый ID ученика.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id, student_id=change_parametr[3:])
        return await callback.answer()
    elif change_parametr.startswith('name'):
        await state.set_state(ChangeStudentInfo.get_student_name)
        callback_message = await callback.message.answer('Напиши ФИО ученика.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[5:])
        return await callback.answer()
    elif change_parametr.startswith('subject'):
        await state.set_state(ChangeStudentInfo.get_student_subject)
        callback_message = await callback.message.answer('Напиши предмет.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[8:])
        return await callback.answer()
    elif change_parametr.startswith('class'):
        await state.set_state(ChangeStudentInfo.get_student_class)
        callback_message = await callback.message.answer('Укажи в каком классе учится твой ученик.',
                                                         reply_markup=await ikb.select_class_student_by_change_keyboard())
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[6:])
        return await callback.answer()
    elif change_parametr.startswith('purpose'):
        await state.set_state(ChangeStudentInfo.get_student_purpose)
        callback_message = await callback.message.answer('Напиши цель.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[8:])
        return await callback.answer()
    elif change_parametr.startswith('price'):
        await state.set_state(ChangeStudentInfo.get_student_price)
        callback_message = await callback.message.answer('Напиши новую цену урока в рублях за час.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[6:])
        return await callback.answer()
    elif change_parametr.startswith('transfer'):
        await state.set_state(ChangeStudentInfo.get_student_transfer)
        callback_message = await callback.message.answer('Напиши ФИО нового трансфера.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[9:])
        return await callback.answer()
    elif change_parametr.startswith('phone'):
        await state.set_state(ChangeStudentInfo.get_student_phone)
        callback_message = await callback.message.answer('Напиши номер телефона.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[6:])
        return await callback.answer()
    elif change_parametr.startswith('platform'):
        await state.set_state(ChangeStudentInfo.get_student_platform)
        callback_message = await callback.message.answer('Напиши название платформы.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[9:])
        return await callback.answer()
    elif change_parametr.startswith('nick'):
        await state.set_state(ChangeStudentInfo.get_student_nick)
        callback_message = await callback.message.answer('Напиши ник ученика на платформе.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[5:])
        return await callback.answer()
    elif change_parametr.startswith('timezone'):
        await state.set_state(ChangeStudentInfo.get_student_timezone)
        callback_message = await callback.message.answer('Напиши часовой пояс ученика относительно Москвы. Например (+3 или -2). Если нужно указать МСК, напиши +0',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='change_student_info_close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(main_message_id=callback.message.message_id, callback_message_id=callback_message_id,
                                student_id=change_parametr[9:])
        return await callback.answer()
