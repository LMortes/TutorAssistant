from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.loader import dp
from bot.utils.mysql import db
from bot.utils.states.add_teacher_state import AddTeacher


@dp.message_handler(Text('👨‍🏫 Добавить репетитора'))
async def add_teacher_handler(message: types.Message, state: FSMContext):
    await state.set_state(AddTeacher.get_user_id)
    await message.answer('Отправь id репетитора')


@dp.message_handler(state=AddTeacher.get_user_id)
async def get_user_id_teacher(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        user_id = int(answer)
    except:
        return await message.answer('Неверный ввод')

    if user_id < 0:
        return await message.answer('Пользователя с таким id не существует. Введи id заного.')
    await state.update_data(teacher_id=user_id)
    await state.set_state(AddTeacher.get_fio)
    await message.answer('Хорошо, я запомнил id репетитора, теперь введи его ФИО')


@dp.message_handler(state=AddTeacher.get_fio)
async def get_fio_teacher(message: types.Message, state: FSMContext):
    fio_text = message.text
    await state.update_data(fio_teacher=fio_text)
    await state.set_state(AddTeacher.get_subject)
    await message.answer('Хорошо, я запомнил ФИО репетитора, теперь пришли мне название предмета, который он преподает')


@dp.message_handler(state=AddTeacher.get_subject)
async def get_subject_teacher(message: types.Message, state: FSMContext):
    subject = message.text
    await state.update_data(subject=subject)
    await message.answer('Отлично, я запишу этого репетитора в базу данных, после чего он сможет авторизоваться в боте')

    data = await state.get_data()
    teacher_id = data.get('teacher_id')
    fio_teacher = data.get('fio_teacher')
    subject = data.get('subject')

    await db.add_new_teacher(teacher_id, fio_teacher, subject)
    await state.reset_data()
    await state.finish()