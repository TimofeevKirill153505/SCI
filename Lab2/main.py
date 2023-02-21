import re

def add(first, second):
    return first+second

def sub(first, second):
    return first-second

def mult(first, second):
    return first * second

def div(first, second):
    return first / second

commands = {"add":add, "div":div, "mult":mult, "sub":sub}

def readnumber():
    numb:str = str()
    regex = r'\d+([\.]\d+)?'
    while not re.match(regex, numb):
        numb:str = input("Enter number\n")

    return numb

def readcommand():
    com = str()
    while not com in commands.keys():
        com = input("Input command:add, sub, mult, div\n")

    return com

print("Hello world!")

first = float(readnumber())
second = float(readnumber())
com = readcommand()

print(commands[com](first, second))