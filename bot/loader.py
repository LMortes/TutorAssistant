import asyncio
from aiocron import crontab
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.utils.other.check_lesson_current_time import run_periodic_check_lesson_current_time
from .config import BOT_TOKEN
from .utils.mysql import db

load_dotenv()

def run_periodic_check_lesson_current_time_wrapper():
    async def wrapped():
        await run_periodic_check_lesson_current_time(bot)
    return wrapped

async def on_startup(_):
    print('Bot started')
    loop = asyncio.get_event_loop()
    await db.connection(loop)
    asyncio.create_task(run_periodic_check_lesson_current_time(bot))
    cron = crontab('* * * * *', func=run_periodic_check_lesson_current_time_wrapper())
    # cron.start()


bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

