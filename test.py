from sqlite import db


def fill_user():
    columns = ("id", "fname", "lname", "user_type")
    values = [
        (331734935, "Firsty", "User", "admin"),
        (832556893, "Second", "User", "user"),
        (322588380, "Third", "Test", "user"),
    ]
    db.insert("users", columns, values)


def fill_project():
    columns = ("name",)
    values = [("Project 1",), ("Project 2",), ("Project 3",)]
    db.insert("objects", columns, values)
