from aiogram import executor
import logging
from hendlers import *


logging.basicConfig(level=logging.INFO)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)