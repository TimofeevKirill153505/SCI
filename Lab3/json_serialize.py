import inspect
import types
import re


def gap_func(string: str):
    out_string: str = ""
    indent: int = 4
    opened_brackets: int = 0
    i: int = 0

    while i < len(string):
        if string[i] == "{" and string[i + 1] != "}":
            if string[i + 1] == " ":
                out_string += string[i] + "\n" + " " * (indent - 1)
            else:
                out_string += string[i] + "\n" + " " * indent
            opened_brackets += 1
            out_string += " " * indent * (opened_brackets - 1)
        elif string[i] == ":" and string[i + 2] == "{" and string[i + 3] != "}":
            out_string += string[i] + "\n" + " " * indent * opened_brackets
            i += 1
        elif string[i] == "}" and string[i - 1] != "{":
            opened_brackets -= 1
            out_string += "\n" + " " * indent * opened_brackets + string[i]
        elif string[i] == ",":
            out_string += string[i] + "\n" + " " * indent * opened_brackets
            i += 1
        else:
            out_string += string[i]
        i += 1

    return out_string


def shield_str(txt: str) -> str:
    txt = txt.replace("\\", "\\\\")
    txt = txt.replace('"', '\\"')
    txt = txt.replace("'", "\\'")
    txt = txt.replace("\n", "\\n")
    txt = txt.replace("\t", "\\t")

    return txt


def change_indent(src: str) -> str:
    while src[:3] != "def":
        src = src.replace("    def", "def", 1)
        src = src.replace("\n    ", "\n")

    return src


def f():
    pass


func = type(f)
module = type(re)
none = type(None)


def serialize(obj):
    default_types = [
        int,
        str,
        bool,
        dict,
        tuple,
        float,
        list,
        set,
        bool,
        type,
        func,
        module,
        type,
        types.CodeType,
        bytes,
        property,
    ]
    if type(obj) in default_types:
        return "{" + basic_serailize(obj) + "}"
    elif type(obj) is not types.NoneType:
        return "{" + serialize_object(obj) + "}"
    else:
        return "{" + serialize_none() + "}"


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
    elif isinstance(obj, types.CodeType):
        return serialize_code(obj)
    elif isinstance(obj, bytes):
        return serialize_bytes(obj)
    elif isinstance(obj, property):
        return serialize_property(obj)
    else:
        return serialize_none()


def type_to_dict(obj: type) -> dict:
    dct = obj.__dict__

    if obj in __builtins__.values():
        ret_dct = {"builtin type": obj.__name__}
        return ret_dct

    ret_dct: dict = {"__name__": obj.__name__}
    for k, v in dct.items():
        if k == "__module__" or k == "__dict__" or k == "__weakref__":
            continue

        ret_dct[k] = v

    ret_dct["parents"] = tuple(obj.mro())[1:]

    if ret_dct["parents"] == (object,):
        ret_dct["parents"] = tuple()
    print(obj.mro())

    return ret_dct


def serialize_property(obj: property):
    tpl = obj.fget, obj.fset, obj.fdel
    return basic.format(type="property", t_p="{}", val=serialize(tpl))


def serialize_none():
    return basic.format(type="none", t_p="{}", val="{}")


def serialize_type(obj: type) -> str:
    # print(obj.__dict__)
    dct = type_to_dict(obj)

    return basic.format(type="type", t_p="{}", val=dict_jsonobj(dct))


def serialize_module(obj):
    val_dict = {}
    line = str(obj)
    srch = re.search(r"\\\\", line)
    if srch is None:
        val_dict["path"] = "basic"
    else:
        val_dict["path"] = re.search(r"from \'(.*)\'", line).group(1)

    val_dict["name"] = re.search(r"module \'([^\']*)\'", line).group(1)

    return basic.format(type="module", t_p="{}", val=dict_jsonobj(val_dict))


def serialize_tuple(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ", "

    val = val[:-2] + "]"
    if val == "]":
        val = "[]"

    return basic.format(type="tuple", val=val, t_p="{}")


def serialize_set(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ", "

    val = val[:-2] + "]"

    return basic.format(type="set", val=val, t_p="{}")


def serialize_bool(obj) -> str:
    return basic.format(type="bool", val=str(obj).lower(), t_p="{}")


def serialize_int(obj) -> str:
    return basic.format(type="int", val=str(obj), t_p="{}")


def serialize_float(obj) -> str:
    return basic.format(type="float", val=str(obj), t_p="{}")


def serialize_string(obj) -> str:
    return basic.format(type="str", val='"' + shield_str(obj) + '"', t_p="{}")


def serialize_dict(obj: dict) -> str:
    val = "["
    for it in obj.items():
        val += '{ "key": ' + serialize(it[0]) + ', "value": ' + serialize(it[1]) + "}, "

    val = val[:-2] + "]"
    if val == "]":
        val = "[]"
    return basic.format(type="dict", val=val, t_p="{}")


def serialize_list(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ", "

    val = val[:-2] + "]"
    if val == "]":
        val = "[]"
    return basic.format(type="list", val=val, t_p="{}")


def serialize_bytes(obj: bytes):
    lst = list(obj)
    return basic.format(type="bytes", t_p="{}", val=str(lst))


def serialize_code(obj: types.CodeType):
    tpl = (
        obj.co_argcount,
        obj.co_posonlyargcount,
        obj.co_kwonlyargcount,
        obj.co_nlocals,
        obj.co_stacksize,
        obj.co_flags,
        obj.co_code,
        obj.co_consts,
        obj.co_names,
        obj.co_varnames,
        "",
        obj.co_name,
        obj.co_firstlineno,
        obj.co_linetable,
        obj.co_freevars,
        obj.co_cellvars,
    )
    # types.CodeType()
    # tpl = {
    #     "__argcount": obj.co_argcount,
    #     "__posonlyargcount": obj.co_posonlyargcount,
    #     "__kwonlyargcount": obj.co_kwonlyargcount,
    #     "__nlocals": obj.co_nlocals,
    #     "__stacksize": obj.co_stacksize,
    #     "__flags": obj.co_flags,
    #     "__codestring": obj.co_code,
    #     "__constants": obj.co_consts,
    #     "__names": obj.co_names,
    #     "__varnames": obj.co_varnames,
    #     "__filename": "",
    #     "__name": obj.co_name,
    #     "__firstlineno": obj.co_firstlineno,
    #     "__linetable": obj.co_linetable,
    #     "__freevars": obj.co_freevars,
    #     "__cellvars": obj.co_cellvars,
    # }
    value = serialize(tpl)
    return basic.format(val=value, type="code", t_p="{}")


def serialize_func(obj: func):
    info = inspect.getclosurevars(obj)
    val_dict = {}
    val_dict["globals"] = dict(info.globals)
    val_dict["argdefs"] = inspect.getfullargspec(obj).defaults
    val_dict["closure"] = tuple([v for k, v in info.nonlocals.items()])
    val_dict["name"] = [
        val for key, val in inspect.getmembers(obj) if key == "__name__"
    ][0]

    val_dict["code"] = obj.__code__

    return basic.format(type="function", val=dict_jsonobj(val_dict), t_p="{}")


def serialize_func2(obj):
    val_dict = {}
    lines = change_indent(inspect.getsource(obj))
    name_regex = r"def\s+(\w+)\s*\("
    func_name = re.search(name_regex, lines)
    val_dict["name"] = func_name.group(1)
    val_dict["source lines"] = lines

    cl_vars = inspect.getclosurevars(obj)
    val_dict["globals"] = dict(cl_vars.globals)
    val_dict["nonlocals"] = dict(cl_vars.nonlocals)

    value = dict_jsonobj(val_dict)

    return basic.format(type="function", val=value, t_p="{}")


def dict_jsonobj(d: dict) -> str:
    rstr = "{"
    # print(d)
    for key, val in d.items():
        # print(key)
        rstr += f'"{key}": {serialize(val)}, '

    rstr = rstr[:-2:]
    rstr += "}"

    return rstr


def serialize_object(obj) -> str:
    type_dict = type_to_dict(type(obj))
    val = obj.__dict__

    return basic.format(
        type="object", t_p=dict_jsonobj(type_dict), val=dict_jsonobj(val)
    )
