import os
import sqlite3
from decimal import Decimal
from datetime import datetime
from typing import Dict, List, Tuple


def adapt_decimal(d):
    return str(d)


def convert_decimal(s):
    return Decimal(s)


# Register the adapter
sqlite3.register_adapter(Decimal, adapt_decimal)

# Register the converter
sqlite3.register_converter("decimal", convert_decimal)

conn = sqlite3.connect(os.path.join("timesheet.db"))
cursor = conn.cursor()


def insert(table: str, columns: Tuple, values: List[Tuple]):
    placeholders = ", ".join("?" * len(columns))
    if len(columns) == 1:
        columns = f"({str(columns[0])})"
    cursor.executemany(
        f"INSERT INTO {table} " f"{columns} " f"VALUES ({placeholders})", values
    )
    conn.commit()


def insert_user(id: int, first_name: str, last_name: str, user_type) -> bool:
    """Добавляет нового пользователя в базу
    возвращает False если пользователь уже есть
    и True в случае успеха"""

    cursor.execute(f"SELECT id FROM users WHERE id={id}")
    user_exists = cursor.fetchall()
    if user_exists:
        return False
    cursor.execute(
        "INSERT INTO users (id, fname, lname, user_type) VALUES (?, ?, ?, ?)",
        (id, first_name, last_name, user_type),
    )
    conn.commit()
    return True


def get_user_type(id: int) -> str:
    cursor.execute(f"SELECT user_type FROM users WHERE id={id}")
    return cursor.fetchone()[0]


def get_users_id_list() -> List[Tuple]:
    """Возвращает список из id зарегистрированных пользователей"""
    cursor.execute("SELECT id, fname, lname, user_type FROM users")
    users = cursor.fetchall()
    return users


def insert_object(object_name: str) -> bool:
    """Добавляет новый объект в базу
    возвращает False если объект уже есть
    и True в случае успеха"""
    cursor.execute(f"SELECT name FROM objects WHERE name='{object_name}'")
    object_exists = cursor.fetchall()

    if object_exists:
        return False
    cursor.execute("INSERT INTO objects (name) VALUES (?)", (object_name,))
    conn.commit()
    return True


def set_actual_object(id_object: int, id_user: int):
    """Добавляет новый текущий объект пользователю"""
    cursor.execute(f"SELECT user FROM actual_object WHERE user={id_user}")
    user_exists = cursor.fetchall()
    if not user_exists:
        cursor.execute(
            "INSERT INTO actual_object (user, object) VALUES (?, ?)",
            (id_user, id_object),
        )
    else:
        cursor.execute(
            f"UPDATE actual_object SET object={id_object} WHERE user={id_user}"
        )
    conn.commit()


def get_actual_object(id_user: int) -> str:
    cursor.execute(f"SELECT object FROM actual_object WHERE user={id_user}")
    object_id = cursor.fetchall()[0][0]
    print(object_id)
    cursor.execute(f"SELECT name FROM objects WHERE id={object_id}")
    return cursor.fetchall()[0][0]


def get_actual_object_id(user_id: int) -> int:
    cursor.execute(f"SELECT object FROM actual_object WHERE user={user_id}")
    return cursor.fetchone()[0]


def get_objects_list() -> List[Tuple]:
    """Возвращает список объектов"""
    cursor.execute("SELECT name FROM objects")
    return cursor.fetchall()


def get_object_id(name: str) -> int:
    """Возвращает id объекта по названию"""
    cursor.execute(f"SELECT id FROM objects WHERE name='{name}'")
    id = cursor.fetchall()[0][0]
    print(id)
    return id


def set_work_date(user_id: int, date: datetime, work_duration: Decimal):
    object = get_actual_object_id(user_id)
    cursor.execute(
        f"SELECT id FROM time WHERE user={user_id} AND day='{date}' AND object={object}"
    )
    result = cursor.fetchone()
    if result:
        cursor.execute(
            f"UPDATE time SET hours={work_duration} WHERE user={user_id} AND day='{date}' AND object={object}"
        )
    else:
        cursor.execute(
            "INSERT INTO time (day, hours, object, user) VALUES (?, ?, ?, ?)",
            (date, work_duration, object, user_id),
        )
    conn.commit()


def _init_db():
    with open("sqlite/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    cursor.execute(
        "SELECT name FROM sqlite_master " "WHERE type='table' AND name='users'"
    )
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
