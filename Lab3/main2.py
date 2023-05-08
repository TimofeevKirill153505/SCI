import serdeser
import re
import inspect
import math
import sys
import os.path
import importlib
import types
import itertools

path = "/home/user/Documents/SCI/Lab3/"
filepath = "D:\SCILabs\SCI\Lab3\kuk.json"


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


class MyClass:
    class_variable = "class_variable"

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def method(self, c):
        return self.a + self.b + c

    @staticmethod
    def static_method(d):
        return d

    @classmethod
    def class_method(cls, e):
        return cls.class_variable + e


class MySubclass(MyClass):
    def method(self, c):
        return 2 * self.a + 2 * self.b + c


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
    t = 3.1415 / 2

    # @dec
    def f(a: int):
        print(8)
        h = t + 7.4
        print(h)
        print(i)
        print(math.sin(i * a + t))
        return "kikiki"

    s = serdeser.Serdeser("json")

    def my_gen():
        for i in range(3):
            yield i

    thing = __builtins__
    if not isinstance(thing, dict):
        thing = thing.__dict__

    gen = types.GeneratorType()
    sa = Sass("a", 1)
    s.dump(MyClass.class_method, filepath)
    func = s.load(filepath)
    print(func("tututu"))
    print(func)


if __name__ == "__main__":
    main()
