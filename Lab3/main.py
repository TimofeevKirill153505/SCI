import serlib
import re
import inspect
import math
import sys
import os.path
import importlib
import types

path = "/home/user/Documents/SCI/Lab3/"


def funcuc():
    cl_var = None

    def uhuhu():
        nonlocal cl_var

    return uhuhu


Cell = type(funcuc().__closure__[0])


class Sass:
    def __init__(self, a: str, b: int):
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

    def __add__(self, other):
        return 1

    def __private(self):
        print("private")

    def _protected():
        print("protected")

    def prpuk(self):
        print(self.__puk)


def dec(func):
    def d(*args):
        print("it's decoratin' time")
        return func(*args)

    return d


i = 5


# @dec


def print_tuple_list(d: list):
    for k, v in d:
        print(str(k) + " : " + str(v))


def print_dict(d: dict):
    for k, v in d.items():
        print(str(k) + " : " + str(v))


def main():
    t = 0

    @dec
    def f(a: int):
        print(8)
        h = 7 + 7.4
        print(h)
        print(i)
        print(math.sin(i * a + t))
        return "kikiki"

    # code = f.__code__
    # for smth in code.co_lines():
    #     print(smth)

    # print(code.co_linetable.__str__())
    # print(code.co_lnotab)

    # print_tuple_list(inspect.getmembers(code))
    # print(f.__closure__)
    # print(f.__globals__)
    code = f.__code__
    gl = dict(inspect.getclosurevars(f).globals)
    gl.update(inspect.getclosurevars(f).nonlocals)
    print(gl)
    defs = inspect.getfullargspec(f).defaults
    closure = inspect.getclosurevars(f).nonlocals

    cells = []
    for key, clvar in closure.items():
        print("closure be like " + str(clvar))
        kkk = Cell(clvar)
        cells.append(kkk)

    fff = types.FunctionType(code, dict(gl), "f", defs, tuple(cells))
    print(fff(7))


if __name__ == "__main__":
    main()
