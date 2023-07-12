from functools import reduce

def tuples_to_string(lst):
    result = ""
    for tpl in lst:
        result += reduce(lambda x, y: str(x) + " " + str(y), tpl, "\n")
    return result
