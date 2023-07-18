import re
from datetime import datetime
from decimal import Decimal
from aiogram import Bot, Dispatcher, Router, types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlite import db
from keyboards import keyboards
from handlers import tools


rt = Router()


@rt.message(
    F.text.regexp(
        r"(0[1-9]|[12][0-9]|3[01])[- \/.](0[1-9]|1[012])[- \/.]((19|20)?\d\d)"
    ).as_("work_date")
)
async def date_record(message: types.Message, work_date: re.Match[str]):
    if len(work_date[3]) == 2:
        year = "20" + work_date[3]
    else:
        year = work_date[3]
    date_str = f"{year}{work_date[2]}{work_date[1]}"
    try:
        date = datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        await message.answer("Неверная дата")
        return

    record = message.text.split()
    if not len(record) == 2:
        await message.answer("Неверный ввод")
        return
    if re.match(r"^\d{1,2}[.,]\d$", record[1]) or re.match(r"^\d{1,2}$", record[1]):
        work_duration = Decimal(record[1].replace(",", "."))
    else:
        await message.answer("Неверный ввод")
        return
    actual_object = db.get_actual_object(message.from_user.id)
    db.set_work_date(message.from_user.id, date, work_duration)
    await message.answer(
        f"{actual_object}\n{date}\nпродолжительность работы - {work_duration} часов"
    )


@rt.message(F.text.regexp(r"^\d{1,2}[.,]\d$"))
async def decimal_record(message: types.Message):
    print("Число с точкой")
    work_duration = Decimal(message.text.replace(",", "."))

    actual_object = db.get_actual_object(message.from_user.id)
    db.set_work_date(message.from_user.id, datetime.today().date(), work_duration)
    await message.answer(
        f"{actual_object}\n{datetime.today().date()}\nпродолжительность работы - {work_duration} часов"
    )


@rt.message(F.text.regexp(r"^\d{1,2}$"))
async def number_record(message: types.Message):
    print("Число")
    work_duration = Decimal(message.text.replace(",", "."))
    actual_object = db.get_actual_object(message.from_user.id)
    db.set_work_date(message.from_user.id, datetime.today().date(), work_duration)
    await message.answer(
        f"{actual_object}\n{datetime.today().date()}\nпродолжительность работы - {work_duration} часов"
    )
