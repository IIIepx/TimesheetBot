import os
import sqlite3
from typing import Dict, List, Tuple


conn = sqlite3.connect(os.path.join("timesheet.db"))
cursor = conn.cursor()


def insert(table: str, columns: Tuple, values: List[Tuple]):
    placeholders = ", ".join("?" * len(columns))
    if len(columns) == 1:
        columns = f"({str(columns[0])})"
    print(f"INSERT INTO {table} {columns} VALUES ({placeholders})")
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
        "INSERT INTO users " "(id, fname, lname, user_type)" "VALUES (?, ?, ?, ?)",
        (id, first_name, last_name, user_type),
    )
    conn.commit
    return True


def get_users_id_list() -> List[Tuple]:
    """Возвращает список из id зарегистрированных пользователей"""
    cursor.execute("SELECT id, fname, lname, user_type FROM users")
    users = cursor.fetchall()
    return users


def insert_object(object_name: str) -> bool:
    """Добавляет новый объект в базу
    возвращает False если объект уже есть
    и True в случае успеха"""
    cursor.execute(f"SELECT name FROM objects WHERE name={object_name}")
    object_exists = cursor.fetchall()

    if object_exists:
        return False
    cursor.execute("INSERT INTO objects (name) VALUES (?)", object_name)
    conn.commit
    return True


def set_actual_object(id_user: int, id_object: int):
    """Добавляет новый текущий объект пользователю"""
    cursor.execute(f"SELECT user FROM actual_objects WHERE user={id_user}")
    user_exists = cursor.fetchall()
    if not user_exists:
        cursor.execute(
            "INSERT INTO actual_objects (user, object) VALUES (?, ?)",
            (id_user, id_object),
        )
    else:
        cursor.execute(
            f"UPDATE actual_objects SET id_object={id_object} WHERE id_user={id_user}"
        )
    conn.commit


def get_objects_list() -> List:
    """Возвращает список объектов"""
    cursor.execute("SELECT name FROM objects")
    return cursor.fetchall()


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
