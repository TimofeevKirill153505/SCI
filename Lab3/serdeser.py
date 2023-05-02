import inspect
import types
import re
import sys
import importlib


class Serdeser:
    def gap_func(self, string: str):
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

    @staticmethod
    def __shield_str(txt: str) -> str:
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

    def serialize(self, obj):
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
            types.FunctionType,
            types.ModuleType,
            type,
            types.CodeType,
            bytes,
            property,
            classmethod,
            staticmethod,
        ]
        if type(obj) in default_types:
            return "{" + self.basic_serailize(obj) + "}"
        elif type(obj) is not types.NoneType:
            return "{" + self.serialize_object(obj) + "}"
        else:
            return "{" + self.serialize_none() + "}"

    basic: str = ' "type": "{type}", "type properties": {t_p}, "value": {val} '

    def basic_serailize(self, obj) -> str:
        # int, float, string, dict, tuple, list, set, type, bool, function
        if isinstance(obj, bool):
            return self.serialize_bool(obj)
        elif isinstance(obj, int):
            return self.serialize_int(obj)
        elif isinstance(obj, float):
            return self.serialize_float(obj)
        elif isinstance(obj, str):
            return self.serialize_string(obj)
        elif isinstance(obj, dict):
            return self.serialize_dict(obj)
        elif isinstance(obj, list):
            return self.serialize_list(obj)
        elif isinstance(obj, set):
            return self.serialize_set(obj)
        elif isinstance(obj, tuple):
            return self.serialize_tuple(obj)
        elif isinstance(obj, types.FunctionType):
            return self.serialize_func(obj)
        elif isinstance(obj, types.FunctionType):
            return self.serialize_module(obj)
        elif isinstance(obj, type):
            return self.serialize_type(obj)
        elif isinstance(obj, types.CodeType):
            return self.serialize_code(obj)
        elif isinstance(obj, bytes):
            return self.serialize_bytes(obj)
        elif isinstance(obj, property):
            return self.serialize_property(obj)
        elif isinstance(obj, staticmethod):
            return self.serialize_staticmethod(obj)
        elif isinstance(obj, classmethod):
            return self.serialize_classmethod(obj)
        else:
            return self.serialize_none()

    def serialize_staticmethod(self, obj: staticmethod):
        func = obj.__func__

        return self.basic.format(
            type="staticmethod", t_p="{}", val=self.serialize(func)
        )

    def serialize_classmethod(self, obj: classmethod):
        func = obj.__func__

        return self.basic.format(type="classmethod", t_p="{}", val=self.serialize(func))

    @staticmethod
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

    def serialize_property(self, obj: property):
        tpl = obj.fget, obj.fset, obj.fdel
        return self.basic.format(type="property", t_p="{}", val=self.serialize(tpl))

    def serialize_none(self):
        return self.basic.format(type="none", t_p="{}", val="{}")

    def serialize_type(self, obj: type) -> str:
        # print(obj.__dict__)
        dct = self.type_to_dict(obj)

        return self.basic.format(type="type", t_p="{}", val=self.dict_to_obj(dct))

    def serialize_module(self, obj):
        val_dict = {}
        line = str(obj)
        srch = re.search(r"\\\\", line)
        if srch is None:
            val_dict["path"] = "basic"
        else:
            val_dict["path"] = re.search(r"from \'(.*)\'", line).group(1)

        val_dict["name"] = re.search(r"module \'([^\']*)\'", line).group(1)

        return self.basic.format(
            type="module", t_p="{}", val=self.dict_to_obj(val_dict)
        )

    def serialize_tuple(self, obj):
        val = "["
        for it in obj:
            val += self.serialize(it) + ", "

        val = val[:-2] + "]"
        if val == "]":
            val = "[]"

        return self.basic.format(type="tuple", val=val, t_p="{}")

    def serialize_set(self, obj):
        val = "["
        for it in obj:
            val += self.serialize(it) + ", "

        val = val[:-2] + "]"

        return self.basic.format(type="set", val=val, t_p="{}")

    def serialize_bool(self, obj) -> str:
        return self.basic.format(type="bool", val=str(obj).lower(), t_p="{}")

    def serialize_int(self, obj) -> str:
        return self.basic.format(type="int", val=str(obj), t_p="{}")

    def serialize_float(self, obj) -> str:
        return self.basic.format(type="float", val=str(obj), t_p="{}")

    def serialize_string(self, obj) -> str:
        return self.basic.format(
            type="str", val='"' + self.__shield_str(obj) + '"', t_p="{}"
        )

    def serialize_dict(self, obj: dict) -> str:
        val = "["
        for it in obj.items():
            val += (
                '{ "key": '
                + self.serialize(it[0])
                + ', "value": '
                + self.serialize(it[1])
                + "}, "
            )

        val = val[:-2] + "]"
        if val == "]":
            val = "[]"
        return self.basic.format(type="dict", val=val, t_p="{}")

    def serialize_list(self, obj):
        val = "["
        for it in obj:
            val += self.serialize(it) + ", "

        val = val[:-2] + "]"
        if val == "]":
            val = "[]"
        return self.basic.format(type="list", val=val, t_p="{}")

    def serialize_bytes(self, obj: bytes):
        lst = list(obj)
        return self.basic.format(type="bytes", t_p="{}", val=str(lst))

    def serialize_code(self, obj: types.CodeType):
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
        value = self.serialize(tpl)
        return self.basic.format(val=value, type="code", t_p="{}")

    def serialize_func(self, obj: func):
        info = inspect.getclosurevars(obj)
        val_dict = {}
        val_dict["globals"] = dict(info.globals)
        val_dict["argdefs"] = inspect.getfullargspec(obj).defaults
        val_dict["closure"] = tuple([v for k, v in info.nonlocals.items()])
        val_dict["name"] = [
            val for key, val in inspect.getmembers(obj) if key == "__name__"
        ][0]

        val_dict["code"] = obj.__code__

        return self.basic.format(
            type="function", val=self.dict_to_obj(val_dict), t_p="{}"
        )

    def dict_to_obj(self, d: dict) -> str:
        rstr = "{"
        # print(d)
        for key, val in d.items():
            # print(key)
            rstr += f'"{key}": {self.serialize(val)}, '

        rstr = rstr[:-2:]
        rstr += "}"

        return rstr

    def serialize_object(self, obj) -> str:
        type_dict = self.type_to_dict(type(obj))
        val = obj.__dict__

        return self.basic.format(
            type="object", t_p=self.dict_to_obj(type_dict), val=self.dict_to_obj(val)
        )

    mod_ind = 0

    @staticmethod
    def deshield_str(txt: str) -> str:
        txt = txt.replace("\\t", "\t")
        txt = txt.replace("\\n", "\n")
        txt = txt.replace('\\"', '"')
        txt = txt.replace("\\'", "'")
        txt = txt.replace("\\\\", "\\")

        # print(txt)
        return txt

    # возвращает кортеж для среза скобок
    @staticmethod
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

    @staticmethod
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

    @classmethod
    def find_value(cls, txt: str) -> tuple[int, int]:
        # print(txt)
        first_symb = re.search(r"[^\s:]", txt)
        val: str = ""
        if txt[first_symb.start()] == '"':
            beg, end = cls.parse_quotes(txt)
            return beg, end

        elif txt[first_symb.start()] == "[":
            return cls.parse_brackets(txt, False)

        elif txt[first_symb.start()] == "{":
            return cls.parse_brackets(txt, True)

        else:
            return re.search(r"[^\s:}]+", txt).span()

    @classmethod
    def parse_to_kv(cls, txt: str) -> dict:
        d = {}
        while True:
            key_match = re.search(r'"[^"]*"', txt)
            if not key_match:
                break
            key = txt[key_match.start() + 1 : key_match.end() - 1]
            txt = txt[key_match.end() : :]
            val_tpl = cls.find_value(txt)
            d[key] = txt[val_tpl[0] : val_tpl[1]]
            txt = txt[val_tpl[1] : :]

        return d

    def deserialize(self, txt: str):
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
            "property",
            "classmethod",
            "staticmethod",
        }
        kv = self.parse_to_kv(txt)
        # print(kv)
        kv["type"] = kv["type"][1:-1]
        if kv["type"] in basic_types:
            return self.basic_deserialize(kv)
        else:
            return self.deserialize_object(kv)

    def basic_deserialize(self, kv):
        t = kv["type"]
        v = kv["value"]

        if t == "str":
            return self.deserialize_string(v)
        elif t == "int":
            return self.deserialize_int(v)
        elif t == "bool":
            return self.deserialize_bool(v)
        elif t == "float":
            return self.deserialize_float(v)
        elif t == "tuple":
            return self.deserialize_tuple(v)
        elif t == "list":
            return self.deserialize_list(v)
        elif t == "set":
            return self.deseialize_set(v)
        elif t == "dict":
            return self.deserialize_dict(v)
        elif t == "function":
            return self.deserialize_function(v)
        elif t == "module":
            return self.deserialize_module(v)
        elif t == "type":
            return self.deserialize_type(v)
        elif t == "code":
            return self.deserialize_code(v)
        elif t == "bytes":
            return self.deserialize_bytes(v)
        elif t == "property":
            return self.deserialize_property(v)
        elif t == "staticmethod":
            return self.deserialize_staticmethod(v)
        elif t == "classmethod":
            return self.deserialize_classmethod(v)
        elif t == "none":
            return None

    def deserialize_classmethod(self, val):
        f = self.deserialize(val)
        return classmethod(f)

    def deserialize_staticmethod(self, val):
        f = self.deserialize(val)
        return staticmethod(f)

    def deserialize_property(self, val):
        tpl = self.deserialize(val)
        return property(*tpl)

    def deserialize_bytes(self, val):
        reg = r"\d+"
        mtchs = re.findall(reg, val)

        lst = []
        for it in mtchs:
            lst.append(int(it))

        return bytes(lst)

    def deserialize_code(self, val):
        tpl = self.deserialize(val)

        return types.CodeType(*tpl)

    def deserialize_type(self, val):
        kv = self.parse_to_kv(val)
        if kv.get("builtin type") is not None:
            v = self.deserialize(kv["builtin type"])
            for bk, bv in __builtins__.items():
                if bk == v:
                    return bv

        for k, v in kv.items():
            # print(k)
            kv[k] = self.deserialize(v)
        name = kv.pop("__name__")
        parents = kv.pop("parents")
        return type(name, parents, kv)

    def deserialize_module(self, val):
        global mod_ind
        kv = self.parse_to_kv(val)
        if kv["path"] != "basic":
            sys.path.insert(mod_ind, self.deserialize(kv["path"]))
            mod_ind += 1

        return importlib.import_module(self.deserialize(kv["name"]))

    def deserialize_function(self, val):
        kv = self.parse_to_kv(val)
        dct = {}
        for k, v in kv.items():
            dct[k] = self.deserialize(v)
        arr = []
        for it in dct["closure"]:
            arr.append(types.CellType(it))

        dct["closure"] = tuple(arr)
        return types.FunctionType(**dct)

    def deserialize_string(self, val) -> str:
        return self.deshield_str(val[1:-1])

    def deserialize_int(self, val) -> int:
        return int(val)

    def deserialize_bool(self, val) -> bool:
        return val == "true"

    def deserialize_float(self, val) -> float:
        return float(val)

    def deserialize_tuple(self, val) -> tuple:
        lst = []

        while True:
            tpl = self.parse_brackets(val, True)
            if tpl[0] == -1:
                break
            lst.append(self.deserialize(val[tpl[0] : tpl[1]]))
            val = val[tpl[1] : :]

        return tuple(lst)

    def deserialize_list(self, val) -> list:
        lst = []

        while True:
            tpl = self.parse_brackets(val, True)
            if tpl[0] == -1:
                break
            lst.append(self.deserialize(val[tpl[0] : tpl[1]]))
            val = val[tpl[1] : :]

        return lst

    def deseialize_set(self, val) -> set:
        lst = []

        while True:
            tpl = self.parse_brackets(val, True)
            if tpl[0] == -1:
                break
            lst.append(self.deserialize(val[tpl[0] : tpl[1]]))
            val = val[tpl[1] : :]

        return set(lst)

    def deserialize_dict(self, val) -> dict:
        d = {}
        while True:
            tpl = self.parse_brackets(val, True)
            if tpl[0] == -1:
                break
            kv = self.parse_to_kv(val[tpl[0] : tpl[1]])
            key = self.deserialize(kv["key"])
            value = self.deserialize(kv["value"])
            d[key] = value
            val = val[tpl[1] : :]

        return d

    def deserialize_object(self, kv) -> str:
        t_p = kv["type properties"]
        type_kv = self.parse_to_kv(t_p)
        for k, v in type_kv.items():
            type_kv[k] = self.deserialize(v)

        parents = type_kv.pop("parents")
        name = type_kv.pop("__name__")
        typ = type(name, parents, type_kv)

        obj = typ.__new__(typ)

        val_kv = self.parse_to_kv(kv["value"])
        for k, v in val_kv.items():
            val_kv[k] = self.deserialize(v)

        obj.__dict__ = val_kv

        return obj
