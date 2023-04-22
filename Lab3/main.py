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
    print(i)
    print(math.sin(i * a))
    return "kikiki"


def main():
    # d = {"one": 1, "string": "str", "float": 1.25, "bool": False,
    #      "set": {1, 2, 3}, "list": [], "tuple": (1, 2, 3), 'empty dict': {}}
    ser = serlib.serialize(f)
    print(ser)
    ff = serlib.deserialize(ser)
    print(ff(1))


if __name__ == "__main__":
    main()
