import json
import yaml
import xml
import pickle
import inspect
import sys
import re

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

        

def main():
    reg = r'g (...)'
    text = 'g jjj g jkl'
    print(re.search(reg, text))
    
    
if __name__ == "__main__":
    main()
