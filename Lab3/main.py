import serdeser
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


class Bass:
    def base():
        print("раз раз раз это хардбас")


class Hard:
    def hard():
        print("yeah boooooah")


class Sass(Hard, Bass):
    def __init__(self, a: str, b: int):
        self.a = a
        self.b = b
        self.__hop = "hop" + a
        self.__poh = "jej" + str(b)

    def method(self):
        return self.a + str(self.b)

    def ppp(self, c: int):
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

    def _protected(self):
        print("protected")

    def prpuk(self):
        print(self.puk)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value * 10

    @classmethod
    def class_method(cls):
        print("this is class " + str(cls))

    @staticmethod
    def static():
        print("i am useless method")

    # @property
    # def __dict__(self):
    #     return {"наёбка для уёбка": "nayobka"}


def dec(func):
    def d(*args):
        print("it's decoratin' time")
        return func(*args)

    return d


i = 5


def print_tuple_list(d: list):
    for k, v in d:
        print(str(k) + " : " + str(v))


def print_dict(d: dict):
    for k, v in d.items():
        print(str(k) + " : " + str(v))


def func(a, b):
    print(a - b)


def to_dict(thing) -> dict:
    dct = {}
    for k, v in thing:
        dct[k] = v

    return dct


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

    i = 2
    ser = serdeser.Serdeser(mode="xml")
    d = {1: "str", "set": {1, 2, 3}, "tuple": (1, 2.78, 3), "bool": False}
    txt = ser.serialize(d)
    print(txt)
    print(ser.deserialize(txt))


if __name__ == "__main__":
    main()
