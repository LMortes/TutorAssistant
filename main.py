from aiogram.utils import executor
from bot.loader import on_startup
from bot.handlers import dp
from bot.utils.other.logging import setup_logger


if __name__ == '__main__':
    setup_logger()
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)