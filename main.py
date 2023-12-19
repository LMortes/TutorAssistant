from aiogram.utils import executor
from bot.loader import on_startup, bot
from bot.handlers import dp


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)