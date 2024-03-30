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
from bot.utils.other.generate_teacher_profile import generate_teacher_profile
from bot.utils.other.parse_registration_date import parse_registration_date

# Настройки для репетитора
# 1) Часовой пояс
# 2) Напоминания
#     2.1) Напоминание до урока(умолчание: выкл)
#     2.2) За сколько минут упоминать?(умолчание: 15)(недоступно при выключенной настройке)
# 3) Настройки налогов
#     3.1) Процент налогов (умолчание 0%)
#     3.2) Отображать вычет налогов в расписании и в профиле?(умолчание: нет)
# 4) Автозаполнение ученика
#     4.1) Автозаполнение(умолчание: выкл)
#     4.2) Все поля которые можно автозаполнить


@dp.message_handler(Text('⚙️ Настройки'))
async def teacher_settings_handler(message: types.Message):
    teacher_tg_id = message.from_user.id
    await message.answer('⚙️ Настройки', reply_markup=await ikb.teacher_settings(teacher_tg_id))


@dp.callback_query_handler(lambda callback: callback.data.startswith('teacher_settings_'))
async def teacher_settings_callback(callback: types.CallbackQuery):
    message_callback = callback.message[17:]

    if message_callback == 'timezone':
        pass
    elif message_callback == 'notifications':
        await callback.message.edit_reply_markup(reply_markup=await ikb.teacher_settings_notifications())
    elif message_callback == 'nalog':
        pass
    elif message_callback == 'auto_zapoln':
        pass