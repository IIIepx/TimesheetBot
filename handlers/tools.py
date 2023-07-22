import pandas as pd
# from pretty_html_table import build_table
from functools import reduce
from typing import Dict, List, Tuple
from datetime import datetime
from sqlite import db
from handlers.pht import build_table


def data_to_html(data: List[Tuple], columns=[], caption=None):
    df = pd.DataFrame.from_records(
        data,
        columns=columns,
        index=list(range(1, len(data) + 1)),
    )
    start = """<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><style>table { width: 100%;}</style><title>Отчет</title></head><body>"""
    end = """ </body></html>"""
    output = (
        start
        + build_table(
            df,
            "blue_dark",
            index=False,
            caption=caption,
            font_size="40px",
            index_align="center",
            width_dict=["70%", "20%"],
            text_align=["left", "right"],
            col_align=["center", "center"],
        ).replace("Итог", """<b>Итог</b>""")
        + end
    )
    return output


def tables_to_html(data: Dict, columns=[]):
    body = ""
    for key, value in data.items():
        body += build_table(
            pd.DataFrame.from_records(value, columns=columns),
            "red_dark",
            index=False,
            caption=key,
            font_size="40px",
            index_align="center",
            width_dict=["70%", "20%"],
            text_align=["left", "right"],
            col_align=["center", "center"],
        )
    start = """<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><style>table { width: 100%;}</style><title>Отчет</title></head><body>"""
    end = """ </body></html>"""
    body = start + body.replace("Итог", """<b>Итог</b>""") + end
    return body


def tuples_to_string(lst):
    result = ""
    for tpl in lst:
        result += reduce(lambda x, y: str(x) + " - " + str(y) + " часов", tpl, "\n")
    return result


def get_list_of_projects():
    lst = db.get_objects_list()
    return [item[0] for item in lst]


def get_month(date: datetime):
    month = date.strftime("%B")
    return month
