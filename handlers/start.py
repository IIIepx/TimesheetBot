from aiogram import Bot, Dispatcher, Router, types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlite import db
from keyboards import keyboards
from handlers import tools

router = Router()
actual_projects = tools.get_list_of_projects()

class UserState(StatesGroup):
    query_access = State()
    project_choice = State()
    query_answer_waiting = State()


@router.message(Command("start"))
async def cmd_start(
        message: types.Message, bot: Bot, dp: Dispatcher, state: FSMContext, root_id: int):
    users = db.get_users_id_list()
    user = [item for item in users if item[0] == message.from_user.id]
    if not user:
        await state.set_state(UserState.query_access)
        await message.answer(
            "Заявка на подсоединение обрабатывается.\n Ожидайте результата."
        )

        await bot.send_message(
            root_id,
            text=f"{message.from_user.first_name} {message.from_user.last_name} подал заявку на подключение",
            reply_markup=keyboards.make_keyboard([
                "Отклонить",
                "Принять как user",
                "Принять как admin",
            ]),
        )
        state_query = dp.fsm.resolve_context(
            bot=bot, chat_id=root_id, user_id=root_id
        )
        await state_query.set_state(UserState.query_answer_waiting)
        await state_query.update_data({"msg": message})


@router.message(UserState.query_answer_waiting, F.text == "Отклонить")
async def claim_reject(message: types.Message, state: FSMContext):
    msg = (await state.get_data())["msg"]
    await message.answer(
        f"Заявка от {msg.from_user.first_name} {msg.from_user.last_name} отклонена",
        reply_markup=types.ReplyKeyboardRemove(),
    )

    await msg.answer("К сожалению ваша заявка отклонена")
    await state.clear()

@router.message(Command("проект"))
async def change_project(message: types.Message, state: FSMContext):
    actual_object = db.get_actual_object(message.from_user.id)
    if actual_object:
        await message.answer(f"Текущий проект - {actual_object}")
    await message.answer("Выберите актуальный проект.", reply_markup=keyboards.make_keyboard(actual_projects))
    await state.set_state(UserState.project_choice)

@router.message(Command("новый"))
async def add_project(message: types.Message):
    user_type = db.get_user_type(message.from_user.id) 
    print(user_type)
    if user_type == "user":
        await message.answer("Эта команда доступна только администраторам")
        return
    project_name = message.text[7:]
    await message.answer(f"Попытка добавления проекта - {project_name}")
    result_insert = db.insert_object(project_name)
    if result_insert:
        await message.answer("Новый проект успешно добавлен.")
        actual_projects = tools.get_list_of_projects()
    else:
        await message.answer("Неудача. Такой проект уже существует.")

@router.message(UserState.query_answer_waiting, F.text.startswith("Принять"))
async def claim_accept(
    message: types.Message, bot: Bot, dp: Dispatcher, state: FSMContext
):
    msg = (await state.get_data())["msg"]
    await message.answer(
        f"Заявка от {msg.from_user.first_name} {msg.from_user.last_name} "
        f"принята, пользователь добавлен",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.clear()
    columns = ("id", "name", "user_type")
    name = msg.from_user.first_name + " " + "" if not msg.from_user.last_name else msg.from_user.last_name 
    values = [(msg.from_user.id, name, message.text.split()[-1])]
    db.insert("users", columns, values)
    await msg.answer(
        f"{message.from_user.first_name} {message.from_user.last_name} "
        f"добавил вас в список пользователей.\n"
        f"Теперь необходимо выбрать проект",
        reply_markup=keyboards.make_keyboard(actual_projects),
    )
    state_query = dp.fsm.resolve_context(
        bot=bot, chat_id=msg.from_user.id, user_id=msg.from_user.id
    )
    await state_query.set_state(UserState.project_choice)


@router.message(UserState.project_choice, F.text.in_(actual_projects))
async def project_accept(message: types.Message, state: FSMContext):

    db.set_actual_object(db.get_object_id(message.text), message.from_user.id)
    await message.answer(
        f"Текущий проект - {message.text}", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(UserState.query_answer_waiting, F.text)
async def wrong_input(message: types.Message):
    await message.answer("Неверный ввод. Заявка пользователя ждет обработки.")


@router.message(UserState.project_choice, F.text)
async def wrong_choice(message: types.Message):
    await message.answer("Неверный ввод. Пожалуйста выберите проект из списка.")
