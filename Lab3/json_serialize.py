import inspect
import functools
import re


def shield_str(txt: str) -> str:
    txt = txt.replace('\\', '\\\\')
    txt = txt.replace('"', '\\"')
    txt = txt.replace("'", "\\'")
    txt = txt.replace('\n', '\\n')
    txt = txt.replace('\t', '\\t')

    return txt


def f():
    pass


func = type(f)


def serialize(obj):
    default_types = [int, str, bool, dict, tuple,
                     float, list, set, bool, type, func]
    if type(obj) in default_types:
        return '{' + basic_serailize(obj) + '}'


basic: str = ' "type": "{type}", "type properties": {t_p}, "value": {val} '


def basic_serailize(obj) -> str:
    # int, float, string, dict, tuple, list, set, type, bool, function
    if isinstance(obj, bool):
        return serialize_bool(obj)
    elif isinstance(obj, int):
        return serialize_int(obj)
    elif isinstance(obj, float):
        return serialize_float(obj)
    elif isinstance(obj, str):
        return serialize_string(obj)
    elif isinstance(obj, dict):
        return serialize_dict(obj)
    elif isinstance(obj, list):
        return serialize_list(obj)
    elif isinstance(obj, set):
        return serialize_set(obj)
    elif isinstance(obj, tuple):
        return serialize_tuple(obj)
    elif isinstance(obj, func):
        return serialize_func(obj)


def serialize_tuple(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ', '

    val = val[:-2] + ']'

    return basic.format(type="tuple", val=val, t_p='{}')


def serialize_set(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ', '

    val = val[:-2] + ']'

    return basic.format(type="set", val=val, t_p='{}')


def serialize_bool(obj) -> str:
    return basic.format(type="bool", val=str(obj).lower(), t_p='{}')


def serialize_int(obj) -> str:
    return basic.format(type="int", val=str(obj), t_p='{}')


def serialize_float(obj) -> str:
    return basic.format(type="float", val=str(obj), t_p='{}')


def serialize_string(obj) -> str:
    return basic.format(type="str", val='"'+shield_str(obj)+'"', t_p='{}')


def serialize_dict(obj: dict) -> str:
    val = '['
    for it in obj.items():
        val += '{ "key": ' + \
            serialize(it[0]) + ', "value": ' + serialize(it[1]) + '}, '

    val = val[:-2] + ']'
    if val == ']':
        val = '[]'
    return basic.format(type="dict", val=val, t_p='{}')


def serialize_list(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ', '

    val = val[:-2] + ']'
    if val == ']':
        val = '[]'
    return basic.format(type="list", val=val, t_p='{}')


def serialize_func(obj):
    val_dict = {}
    lines = inspect.getsource(obj)
    name_regex = r'def\s+(\w+)\s*\('
    func_name = re.match(name_regex, lines)
    val_dict['name'] = func_name.group(1)
    val_dict['source lines'] = lines
    value = dict_jsonobj(val_dict)

    return basic.format(type='function', val=value, t_p='{}')


def dict_jsonobj(d: dict) -> str:
    rstr = '{'
    for key, val in d.items():
        rstr += f'"{key}": {serialize(val)}, '

    rstr = rstr[:-2:]
    rstr += '}'

    return rstr
