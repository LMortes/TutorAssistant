import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.loader import dp, bot
from bot.keyboards import inline as ikb
from bot.utils.mysql import db
from bot.utils.states.add_student_state import AddStudent


async def get_info_student(state):
    data = await state.get_data()
    student_info = {
        'user_id': data.get('user_id'),
        'name': data.get('name'),
        'subject': data.get('subject'),
        'registration_date': data.get('registration_date'),
        'class_student': data.get('class_student'),
        'purpose': data.get('purpose'),
        'price': data.get('price'),
        'transfer': data.get('transfer'),
        'phone': data.get('phone'),
        'platform': data.get('platform'),
        'platform_nick': data.get('platform_nick'),
        'timezone': data.get('timezone'),
        'teacher_id': data.get('teacher_id'),
    }
    return student_info


async def generate_info_student_message(student_info):
    pre_message = '⚙️ Ты вошел в режим добавления нового ученика' \
                  '\nИспользуй кнопки чтобы добавлять информацию об ученике' \
                  '\n\n🔴 Красным кружком помечены поля обязательные для заполнения, остальные по желанию' \
                  '\n\n☑️ После заполнения, нажми "Продолжить" и ученик запишется в базу данных\n' \
                  '✖️ Если надо выйти из режима заполнения ученика нажми на кнопку "Отмена"\n\n'
    info_message = f'{pre_message}Информация об ученике:\n\n' \
                   f'🆔 ID ученика: {"-" if student_info["user_id"] is None else student_info["user_id"]}\n' \
                   f'👦 Имя ученика: {"-" if student_info["name"] is None else student_info["name"]}\n' \
                   f'📚 Предмет: {"-" if student_info["subject"] is None else student_info["subject"]}\n' \
                   f'🔢 Класс: {"-" if student_info["class_student"] is None else student_info["class_student"]}\n' \
                   f'🎯 Цель занятий: {"-" if student_info["purpose"] is None else student_info["purpose"]}\n' \
                   f'💵 Цена урока в час: {"-" if student_info["price"] is None else student_info["price"]}\n' \
                   f'👨 ФИО человека от кого поступают деньги: {"-" if student_info["transfer"] is None else student_info["transfer"]}\n' \
                   f'📞 Номер телефона: {"-" if student_info["phone"] is None else student_info["phone"]}\n' \
                   f'🔗 Платформа: {"-" if student_info["platform"] is None else student_info["platform"]}\n' \
                   f'📩 Ник на платформе: {"-" if student_info["platform_nick"] is None else student_info["platform_nick"]}\n' \
                   f'🕒 Часовой пояс: {student_info["timezone"]}'
    return info_message


async def delete_and_edit_message_add_student(message, state):
    # Добываем ид предыдущих сообщений для последующего удаления
    main_message_id = (await state.get_data()).get('main_message_id')
    callback_message_id = (await state.get_data()).get('callback_message_id')
    student_info = await get_info_student(state)
    info_message = await generate_info_student_message(student_info)
    await message.delete()
    await bot.delete_message(message.chat.id, callback_message_id)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=main_message_id, text=f'{info_message}',
                                reply_markup=await ikb.generate_keyboard_add_student(student_info))
    await state.set_state(AddStudent.add_student_state)  # Устанавливаем состояние редактирования информации ученика


# ------------------------------ Точка входа -----------------------------------
@dp.message_handler(Text('➕ Добавить ученика'))
async def add_student_handler(message: types.Message, state: FSMContext):
    await state.set_state(AddStudent.add_student_state)
    await state.update_data(timezone='+0', teacher_id=message.from_user.id,
                            transfer=None, phone=None, platform=None, platform_nick=None, user_id=None)
    student_info = await get_info_student(state)
    info_message = await generate_info_student_message(student_info)
    main_message = await message.answer(f'{info_message}',
                                        reply_markup=await ikb.generate_keyboard_add_student(student_info))
    main_message_id = main_message.message_id
    await state.update_data(main_message_id=main_message_id)


@dp.callback_query_handler(lambda callback: callback.data == 'close_option', state=['*'])
async def close_option_add_student_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(AddStudent.add_student_state)
    return await callback.answer('Действие отменено')


@dp.message_handler(state=AddStudent.add_student_id)
async def check_id_student(message: types.Message, state: FSMContext):
    answer = message.text
    # Обработка ошибок
    try:
        student_id = int(answer)
    except:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. ID должен состоять только из цифр.')
    if int(student_id) < 0:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. ID пользователя не может быть отрицательным.')

    student_id_exists = await db.get_student_info(student_id)
    if student_id_exists != False:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. Ученик с таким ID уже есть в базе данных.')

    # Запоминаем результат
    await state.update_data(user_id=student_id)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.message_handler(state=AddStudent.add_student_name)
async def check_id_student(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.message_handler(state=AddStudent.add_student_subject)
async def check_id_student(message: types.Message, state: FSMContext):
    subject = message.text
    await state.update_data(subject=subject)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.callback_query_handler(lambda callback: callback.data.startswith('select_class_student_'),
                           state=AddStudent.add_student_class)
async def check_id_student(callback: types.CallbackQuery, state: FSMContext):
    class_student = callback.data[21:]
    await state.update_data(class_student=class_student)

    # Добываем ид предыдущих сообщений для последующего удаления
    main_message_id = (await state.get_data()).get('main_message_id')
    callback_message_id = (await state.get_data()).get('callback_message_id')
    student_info = await get_info_student(state)
    info_message = await generate_info_student_message(student_info)
    await bot.delete_message(callback.message.chat.id, callback_message_id)
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=main_message_id, text=f'{info_message}', \
                                reply_markup=await ikb.generate_keyboard_add_student(student_info))
    await state.set_state(AddStudent.add_student_state)  # Устанавливаем состояние редактирования информации ученика


@dp.message_handler(state=AddStudent.add_student_purpose)
async def check_id_student(message: types.Message, state: FSMContext):
    purpose = message.text
    await state.update_data(purpose=purpose)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.message_handler(state=AddStudent.add_student_price)
async def check_id_student(message: types.Message, state: FSMContext):
    price = message.text
    try:
        validate_price = int(price)
    except:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. Ценник должен быть целым числом.')
    if int(price) < 0:
        await message.delete()
        return await message.answer('❗️ Неверный ввод. Ценник не может быть отрицательным.')
    await state.update_data(price=validate_price)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.message_handler(state=AddStudent.add_student_transfer)
async def check_id_student(message: types.Message, state: FSMContext):
    transfer = message.text
    await state.update_data(transfer=transfer)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.message_handler(state=AddStudent.add_student_phone)
async def check_id_student(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.message_handler(state=AddStudent.add_student_platform)
async def check_id_student(message: types.Message, state: FSMContext):
    platform = message.text
    await state.update_data(platform=platform)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.message_handler(state=AddStudent.add_student_platform_nick)
async def check_id_student(message: types.Message, state: FSMContext):
    platform_nick = message.text
    await state.update_data(platform_nick=platform_nick)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.message_handler(state=AddStudent.add_student_timezone)
async def check_id_student(message: types.Message, state: FSMContext):
    timezone = message.text
    if (timezone == '0' or timezone == '+0'):
        return await message.delete()
    if not timezone.startswith('+'):
        await message.delete()
        return await message.answer(
            '❗️ Неверный ввод. Отсутствует плюс перед числом, или другая синтаксическая ошибка.')
    await state.update_data(timezone=timezone)

    # Удаляем предыдущие сообщения и изменяем главное.
    return await delete_and_edit_message_add_student(message, state)


@dp.callback_query_handler(lambda callback: callback.data.startswith('add_student_'),
                           state=AddStudent.add_student_state)
async def add_student_callback(callback: types.CallbackQuery, state: FSMContext):
    message_callback = callback.data[12:]

    if message_callback == 'id':
        await state.set_state(AddStudent.add_student_id)
        callback_message = await callback.message.answer(
            'Напиши ID ученика в телеграме. Узнать его можно переслав любое сообщение в бота - @username_to_id_bot.\n'
            'Или просто попросить ученика чтобы он написал в этого бота и отправил тебе свой ID\n\n'
            'Если ученика нет в телеграмм и ты хочешь просто добавить его к себе, то ничего не вводи',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text='Отмена', callback_data='close_option')
                ],
            ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()

    elif message_callback == 'name':
        await state.set_state(AddStudent.add_student_name)
        callback_message = await callback.message.answer('Напиши имя ученика или ФИО, на твое усмотрение.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'subject':
        await state.set_state(AddStudent.add_student_subject)
        callback_message = await callback.message.answer(
            'Напиши предмет, который будешь преподавать ученику, если их несколько, напиши через пробел\n'
            'Например: (Математика Русский)',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text='Отмена', callback_data='close_option')
                ],
            ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'class':
        await state.set_state(AddStudent.add_student_class)
        callback_message = await callback.message.answer('Укажи в каком классе учится твой ученик.',
                                                         reply_markup=await ikb.select_class_student_keyboard())
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'purpose':
        await state.set_state(AddStudent.add_student_purpose)
        callback_message = await callback.message.answer('Напиши цель занятий с учеником или какие-то пометки.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'price':
        await state.set_state(AddStudent.add_student_price)
        callback_message = await callback.message.answer('Напиши цену урока в рублях за час.\n'
                                                         'Если время урока другое, то во всей статистике бот сам расчитает стоимость урока, достаточно лишь указать это в настройках',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'transfer':
        await state.set_state(AddStudent.add_student_transfer)
        callback_message = await callback.message.answer(
            'Напиши имя или ФИО человека от кого поступают деньги за урок.\n'
            'Этот пункт заполняется по желанию.',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text='Отмена', callback_data='close_option')
                ],
            ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'phone':
        await state.set_state(AddStudent.add_student_phone)
        callback_message = await callback.message.answer(
            'Напиши номер телефона ученика или родителя ученика в любом формате.\n'
            'Если над указать несколько номеров, то раздели их пробелом.\n'
            'Например: (89009009090 89009009090)',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text='Отмена', callback_data='close_option')
                ],
            ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'platform':
        await state.set_state(AddStudent.add_student_platform)
        callback_message = await callback.message.answer('Напиши на какой платформе ты ведешь занятия с учеником.',
                                                         reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                                                             [
                                                                 types.InlineKeyboardButton(text='Отмена',
                                                                                            callback_data='close_option')
                                                             ],
                                                         ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'platform_nick':
        await state.set_state(AddStudent.add_student_platform_nick)
        callback_message = await callback.message.answer(
            'Напиши ник ученика на платформе, на которой занимаешься с ним.',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text='Отмена', callback_data='close_option')
                ],
            ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'timezone':
        await state.set_state(AddStudent.add_student_timezone)
        callback_message = await callback.message.answer(
            'Напиши часовой пояс ученика относительно Москвы. Например (+3 или -2)\n'
            'Если указать 0 или ничего не указывать, останется по умолчанию +0 (мск)',
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [
                    types.InlineKeyboardButton(text='Отмена', callback_data='close_option')
                ],
            ]))
        callback_message_id = callback_message.message_id
        await state.update_data(callback_message_id=callback_message_id)
        return await callback.answer()
    elif message_callback == 'close':
        await callback.message.delete()
        await callback.answer('Действие отменено')
        return await state.finish()

    elif message_callback == 'continue':
        info_students = await get_info_student(state)
        if (info_students["name"] is not None) \
                and (info_students["subject"] is not None) \
                and (info_students["class_student"] is not None) \
                and (info_students["purpose"] is not None) \
                and (info_students["price"] is not None) \
                and (info_students["platform"] is not None):
            await callback.message.delete()
            await callback.message.answer('Проверьте верно ли вы заполнили информацию об ученике.\n\n'
                                          f'{(await generate_info_student_message(info_students))[332:]}', reply_markup=ikb.ikb_confirm_add_student)
            return await callback.answer()
        else:
            return await callback.answer('❌ Некоторые из обязательных полей не были заполнены.')


@dp.callback_query_handler(lambda callback: callback.data.startswith('confirm_add_student_'), state=AddStudent.add_student_state)
async def confirm_add_student_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data[20:] == 'accept':
        info_student = await state.get_data()
        student_id = info_student["user_id"]
        # Если репетитор не ввел id ученика, то будет генерироваться новый id ученика
        if student_id == None:
            random_student_id_exists = True
            while random_student_id_exists != False:
                random_student_id = random.randint(1000, 9999)
                random_student_id_exists = await db.get_student_info(random_student_id)
            info_student["user_id"] = random_student_id

        is_add_student = await db.add_new_student(info_student)
        if is_add_student:
            await callback.message.delete()
            await state.finish()
            return await callback.message.answer('🥳 Ученик успешно добавлен в базу данных.')
        else:
            await callback.message.delete()
            await state.finish()
            return await callback.message.answer('🙁 Произошла ошибка при добавлении ученика в базу. Возможно вы пытаетесь добавить ученика, который уже привязан к Вам. (id ученика уже есть в базе)')
    elif callback.data[20:] == 'cancel':
        await state.finish()
        return await callback.message.delete()
