import asyncio
import logging


from aiogram import Bot, Dispatcher
from hendler import router
from start_name import TOKEN
#Вставь токен бота в файле start_name и API_TOKEN

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)
if __name__ == '__main__':

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выключение.......')


