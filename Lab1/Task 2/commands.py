import file_module as f_m
import re

curr_container:set = {}

curr_usr:str = None

def do_commands(usr:str)->bool:
    global curr_usr
    curr_usr = usr
    commands:dict = {"add":add, "remove":remove, "find":find, "list":lst, 
                     "grep":grep, "save":save, "load":load, "switch":switch, 
                     "helpme":helpme}
    while True:
        cl_text = input("Enter command\n")
        if cl_text == ":q":
            return False
        
        reg:str = r"(\w+)\s+(\"(.+)\")?"
        match = re.match(reg, cl_text)

        if match == None :
            print("Try again. Enter heplme for documentation")
            
        command = match.group(1)
        if command in commands.keys():
            stay = commands[command](match.group(3))

            if stay != None: return True 


def add(arg:str):
    curr_container.update(arg)
    pass

def remove(arg:str):
    curr_container.difference_update(arg)

def find(arg:str):
    return arg in curr_container

def lst(arg:str):
    for element in curr_container:
        print(element)

def grep(arg:str):
    no_such_el:bool = True
    for element in curr_container:
        if(re.match(arg, element)):
            print(element)
            no_such_el = False

    if no_such_el: print("No such elements")

def save(args:str):
    f_m.save_container(curr_usr, curr_container)

def load(args:str):
    global curr_container
    curr_container = f_m.get_set(curr_usr)

def switch(args:str):
    global curr_container
    global curr_usr
    curr_usr = None
    curr_container = {}

def helpme(args:str):
    pass