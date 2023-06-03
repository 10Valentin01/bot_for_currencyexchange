import logging
from aiogram import executor
from handlers.users import dp


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)


