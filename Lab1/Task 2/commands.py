import file_module as f_m
import re

curr_container:set = set()

curr_usr:str = None

reg:str = r"(\w+)(\s+(.*))?"
arg_reg:str = r'(?:\"(?:[^"]+)\"|(?:\S+))'

def do_commands(usr:str)->bool:
    global curr_usr
    global curr_cont
    curr_usr = usr
    print("Do you wnat to load y/n?")
    choice = input()
    if choice == 'y':
        load("")
    commands:dict = {"add":add, "remove":remove, "find":find, "list":lst, 
                     "grep":grep, "save":save, "load":load, "switch":switch, 
                     "helpme":helpme}
    while True:
        cl_text = input("Enter command\n")
        if cl_text == ":q":
            print("Do you wnat to save y/n?")
            choice = input()
            if choice == 'y':
                save('')
            return False
        
        match = re.match(reg, cl_text)

        if match is None :
            print("Try again. Enter heplme for documentation")
            continue
            
        command = match[1]

        if command in commands:
            stay = commands[command](match[3])
            if stay != None: return True 
        else:
            print("There is no such command. Type helpme for documentation")


def add(com_match):
    global curr_container
    if com_match is None:
        print('arg error')
        return
    
    args = re.findall(arg_reg, com_match)
    for arg_match in args:
        text = arg_match
        if text[0] == '"':
            text = text[1:-1]
        curr_container.add(text)



def remove(com_match:str):
    global curr_container
    if com_match is None:
        print('arg error')
        return
    
    args = re.findall(arg_reg, com_match)
    for arg_match in args:
        text = arg_match
        if text[0] == '"':
            text = text[1:-1]
        curr_container.difference_update({text})

def find(com_match:str):
    if com_match is None:
        print('arg error')
        return
    
    args = re.findall(arg_reg, com_match)
    for arg_match in args:
        text = arg_match
        if text[0] == '"':
            text = text[1:-1]
        if text in curr_container:
            print(text + " is in current container")
        else:
            print(text + " is not in current container")


def lst(arg:str):
    for element in curr_container:
        print(element)

def grep(arg:str):
    if arg is None:
        print('arg error')
        return
    
    bl = False
    for element in curr_container:
        if(re.match(r'\b' + arg + r'\b', element)):
            print(element)
            bl = True
            
        
    if bl is not True:
        print("No such elements")

def save(args:str):
    f_m.save_container(curr_usr, curr_container)

def load(args:str):
    global curr_container
    curr_container.update(f_m.get_set(curr_usr))

def switch(args:str):
    global curr_container
    global curr_usr
    print("Do you wnat to save y/n?")
    choice = input()
    if choice == 'y':
        save('')
    curr_usr = None
    curr_container = set()

    return "smth"

def helpme(args:str):
    print(
    """Format: <command> <args>
    Commands: 
    add <arg>
    remove <arg>
    save
    load
    grep <arg>
    list
    find <arg>
    switch
    helpme""")
