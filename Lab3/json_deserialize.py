import re
import sys
import importlib
import types


def f():
    pass


def funcuc():
    cl_var = None

    def uhuhu():
        nonlocal cl_var

    return uhuhu


Cell = type(funcuc().__closure__[0])

func = type(f)

mod_ind = 0


def deshield_str(txt: str) -> str:
    txt = txt.replace("\\t", "\t")
    txt = txt.replace("\\n", "\n")
    txt = txt.replace('\\"', '"')
    txt = txt.replace("\\'", "'")
    txt = txt.replace("\\\\", "\\")

    # print(txt)
    return txt


# возвращает кортеж для среза скобок
def parse_brackets(text: str, is_figure: bool) -> tuple[int, int]:
    begin = -1
    end = -1
    count = 0
    bracket = r"[]"
    if is_figure:
        bracket = r"{}"
    flag = False
    for n, ch in enumerate(text):
        if ch == '"' and text[n - 1] != "\\":
            flag = not flag
        if ch == bracket[0] and not flag:
            count += 1
            if begin == -1:
                begin = n
        if ch == bracket[1] and not flag:
            count -= 1
            if count == 0:
                end = n + 1
                break

    return begin, end


def parse_quotes(txt) -> tuple[int, int]:
    begin = -1
    end = -1
    flag = True
    for n, ch in enumerate(txt):
        if ch == '"' and (txt[n - 1] != "\\" or n == 0):
            if begin == -1:
                begin = n
            else:
                end = n + 1
                break

    return begin, end


def find_value(txt: str) -> tuple[int, int]:
    # print(txt)
    first_symb = re.search(r"[^\s:]", txt)
    val: str = ""
    if txt[first_symb.start()] == '"':
        beg, end = parse_quotes(txt)
        return beg, end

    elif txt[first_symb.start()] == "[":
        return parse_brackets(txt, False)

    elif txt[first_symb.start()] == "{":
        return parse_brackets(txt, True)

    else:
        return re.search(r"[^\s:}]+", txt).span()


def parse_to_kv(txt: str) -> dict:
    d = {}
    while True:
        key_match = re.search(r'"[^"]*"', txt)
        if not key_match:
            break
        key = txt[key_match.start() + 1 : key_match.end() - 1]
        txt = txt[key_match.end() : :]
        val_tpl = find_value(txt)
        d[key] = txt[val_tpl[0] : val_tpl[1]]
        txt = txt[val_tpl[1] : :]

    return d


def deserialize(txt: str):
    basic_types = {
        "str",
        "dict",
        "tuple",
        "function",
        "bool",
        "set",
        "int",
        "float",
        "type",
        "list",
        "function",
        "module",
        "type",
        "none",
        "code",
        "bytes",
    }
    kv = parse_to_kv(txt)
    # print(kv)
    kv["type"] = kv["type"][1:-1]
    if kv["type"] in basic_types:
        return basic_deserialize(txt, kv)


def basic_deserialize(txt: str, kv):
    t = kv["type"]
    v = kv["value"]

    if t == "str":
        return deserialize_string(v)
    elif t == "int":
        return deserialize_int(v)
    elif t == "bool":
        return deserialize_bool(v)
    elif t == "float":
        return deserialize_float(v)
    elif t == "tuple":
        return deserialize_tuple(v)
    elif t == "list":
        return deserialize_list(v)
    elif t == "set":
        return deseialize_set(v)
    elif t == "dict":
        return deserialize_dict(v)
    elif t == "function":
        return deserialize_function(v)
    elif t == "module":
        return deserialize_module(v)
    elif t == "type":
        return deserialize_type(v)
    elif t == "code":
        return deserialize_code(v)
    elif t == "bytes":
        return deserialize_bytes(v)
    elif t == "none":
        return None


def deserialize_bytes(val):
    reg = r"\d+"
    mtchs = re.findall(reg, val)

    lst = []
    for it in mtchs:
        lst.append(int(it))

    return bytes(lst)


def deserialize_code(val):
    tpl = deserialize(val)

    return types.CodeType(*tpl)


def deserialize_type(val):
    kv = parse_to_kv(val)
    for k, v in kv.items():
        # print(k)
        kv[k] = deserialize(v)

    return type(kv["__name__"], (), kv)


def deserialize_module(val):
    global mod_ind
    kv = parse_to_kv(val)
    if kv["path"] != "basic":
        sys.path.insert(mod_ind, deserialize(kv["path"]))
        mod_ind += 1

    return importlib.import_module(deserialize(kv["name"]))


def deserialize_function(val):
    kv = parse_to_kv(val)
    dct = {}
    for k, v in kv.items():
        dct[k] = deserialize(v)
    arr = []
    for it in dct["closure"]:
        arr.append(Cell(it))

    dct["closure"] = tuple(arr)
    return types.FunctionType(**dct)


def deserialize_function2(val):
    kv = parse_to_kv(val)
    func_name = deserialize(kv["name"])
    func_lines = deserialize(kv["source lines"])

    gl: dict = deserialize(kv["globals"])
    nonl: dict = deserialize(kv["nonlocals"])
    gl.update(nonl)

    def __smth__(*args):
        nonlocal gl
        rv = None

        def chngrv(val):
            nonlocal rv
            rv = val

        gl.update({"__chngrv__": chngrv, "__args__": args})
        exec(func_lines + f"\n__chngrv__({func_name}(*__args__))", gl)

        return rv

    return __smth__


def deserialize_string(val) -> str:
    return deshield_str(val[1:-1])


def deserialize_int(val) -> int:
    return int(val)


def deserialize_bool(val) -> bool:
    return val == "true"


def deserialize_float(val) -> float:
    return float(val)


def deserialize_tuple(val) -> tuple:
    lst = []

    while True:
        tpl = parse_brackets(val, True)
        if tpl[0] == -1:
            break
        lst.append(deserialize(val[tpl[0] : tpl[1]]))
        val = val[tpl[1] : :]

    return tuple(lst)


def deserialize_list(val) -> list:
    lst = []

    while True:
        tpl = parse_brackets(val, True)
        if tpl[0] == -1:
            break
        lst.append(deserialize(val[tpl[0] : tpl[1]]))
        val = val[tpl[1] : :]

    return lst


def deseialize_set(val) -> set:
    lst = []

    while True:
        tpl = parse_brackets(val, True)
        if tpl[0] == -1:
            break
        lst.append(deserialize(val[tpl[0] : tpl[1]]))
        val = val[tpl[1] : :]

    return set(lst)


def deserialize_dict(val) -> dict:
    d = {}
    while True:
        tpl = parse_brackets(val, True)
        if tpl[0] == -1:
            break
        kv = parse_to_kv(val[tpl[0] : tpl[1]])
        key = deserialize(kv["key"])
        value = deserialize(kv["value"])
        d[key] = value
        val = val[tpl[1] : :]

    return d
