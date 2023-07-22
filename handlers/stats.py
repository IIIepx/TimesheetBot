import re
from aiogram import Router, types
from aiogram.types import BufferedInputFile
from aiogram.filters import Command
from sqlite import db
from handlers import tools

rt = Router()


@rt.message(Command("итог"))
async def cmd_result(message: types.Message):
    cmd_list = message.text.split()
    if len(cmd_list) == 1:
        result = db.get_user_detail_result(message.from_user.id)
        if not result:
            await message.answer("Нет данных для формирования отчета")
            return
        output = tools.data_to_html(
            result,
            columns=["Дата", "Кол-во часов"],
            caption=db.get_actual_object(message.from_user.id),
        )

    elif cmd_list[1] == "общий":
        user_type = db.get_user_type(message.from_user.id)
        if user_type == "user":
            result = db.get_user_result(message.from_user.id)
            if not result:
                await message.answer("Нет данных для формирования отчета")
                return

            output = tools.data_to_html(
                result, columns=["Наименование проекта", "Кол-во часов"]
            )
            f = BufferedInputFile(str.encode(output), filename="Отчет.html")
            await message.answer_document(f)
        else:
            result = db.get_objects_result()
            output = tools.tables_to_html(result, columns=["Работник", "Кол-во часов"])
    f = BufferedInputFile(str.encode(output), filename="Отчет.html")
    await message.answer_document(f)
