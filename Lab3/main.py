import serlib
import re
import inspect
import math
import sys
import os.path
import importlib

path = "/home/user/Documents/SCI/Lab3/"


class Sass:
    def __init__(self, a:str, b:int):
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
        print ('private')
        
    def _protected():
        print('protected')
    
    def prpuk(self):
        print(self.__puk)
    

i = 5


def f(a: int):
    print(8)
    h = 7 + 7.4
    print(h)
    print(i)
    print(math.sin(i * a))
    return "kikiki"

def print_tuple_list(d:list):
    for k,v in d:
        print(str(k) + " : " + str(v))
        
def print_dict(d:dict):
    for k,v in d.items():
        print(str(k) + " : " + str(v))
        

def main():
    # d = {"one": 1, "string": "str", "float": 1.25, "bool": False,
    #      "set": {1, 2, 3}, "list": [], "tuple": (1, 2, 3), 'empty dict': {}}
    # ser = serlib.serialize(f)
    # print(ser)
    # ff = serlib.deserialize(ser)
    # print(ff(1))
    t:type = Sass
    s = Sass('ggg', 3)
    # print(dir(s))
    # print(dir(Sass))
    # print(vars(s))
    # print(vars(Sass))
    # print_tuple_list(inspect.getmembers(t))
    # print()
    
    # print_dict(t.__dict__)
    sr = serlib.serialize(Sass)
    print(sr)
    print()
    print()
    t = serlib.deserialize(sr)
    s = t('ggg', 3)
    s.ppp(6)
    print(t)
    
    
    #print(type(s.__dict__))
   
    print()
   # print_dict(s.__dict__)
    print()

    


if __name__ == "__main__":
    main()
