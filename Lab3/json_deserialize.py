import re


# возвращает кортеж для среза скобок
def parse_brackets(text: str, is_figure: bool) -> tuple[int, int]:
    begin = -1
    end = -1
    count = 0
    bracket = r'[]'
    if is_figure:
        bracket = r'{}'

    for n, ch in enumerate(text):

        if ch == bracket[0]:
            count += 1
            if begin == -1:
                begin = n
        if ch == bracket[1]:
            count -= 1
            if count == 0:
                end = n + 1
                break

    return begin, end


def find_value(txt: str) -> tuple[int, int]:
    first_symb = re.search(r'[^\s:]', txt)
    val: str = ""
    if txt[first_symb.start()] == '"':
        srch = re.search(r'"(?:[^"]|(?<=\\)")*"', txt)
        return srch.span()

    elif txt[first_symb.start()] == '[':
        return parse_brackets(txt, False)

    elif txt[first_symb.start()] == '{':
        return parse_brackets(txt, True)

    else:
        return re.search(r'[^\s:}]+', txt).span()


def parse_to_kv(txt: str) -> dict:
    d = {}
    while True:
        key_match = re.search(r'"[^"]*"', txt)
        if not key_match:
            break
        key = txt[key_match.start() + 1: key_match.end() - 1]
        txt = txt[key_match.end()::]
        val_tpl = find_value(txt)
        d[key] = txt[val_tpl[0]:val_tpl[1]]
        txt = txt[val_tpl[1]::]

    return d


def deserialize(txt: str):
    basic_types = {"str", "dict", "tuple",
                   "function", "bool", "set",
                   "int", "float", "type", "list"
                   }
    kv = parse_to_kv(txt)
    # print(kv)
    kv['type'] = kv['type'][1:-1]
    if kv['type'] in basic_types:
        return basic_deserialize(txt, kv)


def basic_deserialize(txt: str, kv):
    t = kv['type']
    v = kv['value']

    if t == 'str':
        return deserialize_string(v)
    elif t == 'int':
        return deserialize_int(v)
    elif t == 'bool':
        return deserialize_bool(v)
    elif t == "float":
        return deserialize_float(v)
    elif t == 'tuple':
        return deserialize_tuple(v)
    elif t == 'list':
        return deserialize_list(v)
    elif t == 'set':
        return deseialize_set(v)
    elif t == 'dict':
        return deserialize_dict(v)
    else:
        return None


def deserialize_string(val) -> str:
    return val[1:-1]


def deserialize_int(val) -> int:
    return int(val)


def deserialize_bool(val) -> bool:
    return val == 'true'


def deserialize_float(val) -> float:
    return float(val)


def deserialize_tuple(val) -> tuple:
    lst = []

    while True:
        tpl = parse_brackets(val, True)
        if tpl[0] == -1:
            break
        lst.append(deserialize(val[tpl[0]: tpl[1]]))
        val = val[tpl[1]::]

    return tuple(lst)


def deserialize_list(val) -> list:
    lst = []

    while True:
        tpl = parse_brackets(val, True)
        if tpl[0] == -1:
            break
        lst.append(deserialize(val[tpl[0]: tpl[1]]))
        val = val[tpl[1]::]

    return lst


def deseialize_set(val) -> set:
    lst = []

    while True:
        tpl = parse_brackets(val, True)
        if tpl[0] == -1:
            break
        lst.append(deserialize(val[tpl[0]: tpl[1]]))
        val = val[tpl[1]::]

    return set(lst)


def deserialize_dict(val) -> dict:
    d = {}
    while True:
        tpl = parse_brackets(val, True)
        if tpl[0] == -1:
            break
        kv = parse_to_kv(val[tpl[0]:tpl[1]])
        key = deserialize(kv['key'])
        value = deserialize(kv['value'])
        d[key] = value
        val = val[tpl[1]::]

    return d
