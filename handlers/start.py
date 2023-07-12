import sys
from aiogram import Router, types
from aiogram.filters import Command
from sqlite import db

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    users = db.get_users_id_list()
    print(str(users))

    await message.answer(str(users))


@router.message(Command("down"))
async def cmd_down(message: types.Message):
    # sys.exit()
    pass
