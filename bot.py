import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from handlers import start
import test

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ["BOT_API"])
dp = Dispatcher()
dp.include_router(start.router)


@dp.message(Command("новый"))
async def cmd_new(message: types.Message):
    await message.answer("Будет добавлен новый объект")


@dp.message(Command("справка"))
async def cmd_help(message: types.Message):
    await message.answer("Здесь будет помощь")


@dp.message(Command("выбор"))
async def cmd_get(message: types.Message):
    await message.answer("Выбор объекта")


@dp.message(Command("итог"))
async def cmd_result(message: types.Message):
    await message.answer("Отработано")


@dp.message(Command("импорт"))
async def cmd_import(message: types.Message):
    await message.answer("Импорт")


@dp.message(Command("тест"))
async def cmd_test(message: types.Message):
    await message.answer(message.text)


@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    await message.answer(
        f"user_id - {message.from_user.id}\n first_name - {message.from_user.first_name}"
    )


async def main():
    # test.fill_user()
    test.fill_project()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
