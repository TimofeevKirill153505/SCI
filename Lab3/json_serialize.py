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

def change_indent(src:str) -> str:
    while(src[:3] != 'def'):
        src = src.replace('    def', 'def', 1)
        src = src.replace('\n    ', '\n')
    
    return src

def f():
    pass


func = type(f)
module = type(re)
none = type(None)


def serialize(obj):
    default_types = [int, str, bool, dict, tuple,
                     float, list, set, bool, type,
                     func, module, type]
    if type(obj) in default_types:
        return '{' + basic_serailize(obj) + '}'
    else:
        return '{' + serialize_none() + '}'


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
    elif isinstance(obj, module):
        return serialize_module(obj)
    elif isinstance(obj, type):
        return serialize_type(obj)
    else:
        return serialize_none()

def type_to_dict(obj:type) -> dict:
    dct = obj.__dict__
    
    ret_dct:dict = {'__name__': obj.__name__}
    for k,v in dct.items():
        if k == '__module__':
            continue
        
        ret_dct[k] = v

        # print(ret_dct)
    return ret_dct
        
def serialize_none():
    return basic.format(type='none', t_p='{}', val='{}')

def serialize_type(obj:type) -> str:
    # print(obj.__dict__)
    dct = type_to_dict(obj)
    
    return basic.format(type='type', t_p='{}', val = dict_jsonobj(dct))
        

def serialize_module(obj):
    val_dict = {}
    line = str(obj)
    srch = re.search(r'\\\\', line)
    if srch is None:
        val_dict['path'] = 'basic'
    else:
        val_dict['path'] = re.search(r'from \'(.*)\'', line).group(1)

    val_dict['name'] = re.search(r'module \'([^\']*)\'', line).group(1)

    return basic.format(type='module', t_p='{}', val=dict_jsonobj(val_dict))


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
    lines = change_indent(inspect.getsource(obj))
    name_regex = r'def\s+(\w+)\s*\('
    func_name = re.search(name_regex, lines)
    val_dict['name'] = func_name.group(1)
    val_dict['source lines'] = lines

    cl_vars = inspect.getclosurevars(obj)
    val_dict['globals'] = dict(cl_vars.globals)
    val_dict['nonlocals'] = dict(cl_vars.nonlocals)

    value = dict_jsonobj(val_dict)

    return basic.format(type='function', val=value, t_p='{}')


def dict_jsonobj(d: dict) -> str:
    rstr = '{'
    for key, val in d.items():
        rstr += f'"{key}": {serialize(val)}, '

    rstr = rstr[:-2:]
    rstr += '}'

    return rstr
