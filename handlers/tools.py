from functools import reduce
from sqlite import db
from datetime import datetime


def tuples_to_string(lst):
    result = ""
    for tpl in lst:
        result += reduce(lambda x, y: str(x) + " " + str(y), tpl, "\n")
    return result


def get_list_of_projects():
    lst = db.get_objects_list()
    return [item[0] for item in lst]


def str_to_date(date_str: str):
    pass
