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




@dp.message_handler(Text("📊 Профиль"))
async def profile_teacher_handler(message: types.Message):
    teacher_info = await db.get_teacher_info_by_id(message.from_user.id)
    profile_text = await generate_teacher_profile(teacher_info)
    await message.answer(profile_text)