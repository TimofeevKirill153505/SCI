import serlib
import re
import inspect
import math
import sys
import os.path
import importlib

path = "/home/user/Documents/SCI/Lab3/"


class Sass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.__hop = "hop" + a
        self.__poh = "jej" + str(b)

    def method(self):
        return self.a + str(self.b)

    def ppp(self, c):
        print(str(c) + self.a + str(self.b))

        """
        format:
        {
            "type":"typename",
            "type properties":{...},
            //"field":value
        }
        """


i = 5


def f(a: int):
    print(8)
    h = 7 + 7.4
    print(h)
    print(math.sin(i * a))
    return "kikiki"


def main():
    # d = {"one": 1, "string": "str", "float": 1.25, "bool": False,
    #      "set": {1, 2, 3}, "list": [], "tuple": (1, 2, 3), 'empty dict': {}}
    # ser = serialize(d)
    # print(ser)
    # print("\n\n")
    # print(deserialize(ser))
    src = inspect.getsource(f)
    print(src)

    # f_str = serialize(f)
    # print(f_str)
    # smth = deserialize(f_str)
    # print(smth(78))
    # print(f.__closure__)
    # print(f.__module__)
    d = dict(inspect.getclosurevars(f).globals)

    sys.path.insert(0, 'D:\\Mcha\\Lab11Py\\')
    # pol = importlib.import_module('Polynom', 'D:\\Mcha\\Lab11Py')
    # print(f.__builtins__)
    import Polynom
    # print(math.__file__)
    juj = serlib.serialize(Polynom)
    print(juj)
    mod = serlib.deserialize(juj)
    print(mod)


if __name__ == "__main__":
    main()
