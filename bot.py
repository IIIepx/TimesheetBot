import os
import sys
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, timereg, stats
from sqlite import db


load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

root_id = int(os.environ["ROOT_USER"])

bot = Bot(token=os.environ["BOT_API"])
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start.router)
dp.include_router(timereg.rt)
dp.include_router(stats.rt)


@dp.message(Command("q"))
async def cmd_down(message: types.Message):
    user_type = db.get_user_type(message.from_user.id)
    if user_type == "user":
        await message.answer("Недостаточно прав")
        return
    await message.answer("Shutdown bot. Buy")
    sys.exit()


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    f = open("help.txt", "r")
    str = f.read()
    await message.answer(str, parse_mode="HTML")


async def main():
    await dp.start_polling(bot, dp=dp, root_id=root_id)


if __name__ == "__main__":
    asyncio.run(main())
