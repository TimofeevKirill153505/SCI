import json

filename:str = "/home/user/Documents/SCI/Lab1/Task 2/data.json"

def get_all()->dict:
    file = open(filename)
    all_dict:dict = json.load(file)
    file.close()
    for elmnt in all_dict.items():
        all_dict[elmnt[0]] = set(elmnt[1])
    return all_dict


def get_users()->set:
    file = open(filename)
    usrs = json.load(file).keys()
    file.close()
    return set(usrs)


def get_set(username:str)->set:
    file = open(filename)
    usr_set = json.load(file)[username]
    file.close()
    return set(usr_set)


def save_container(username:str, container:set):
    all_dict:dict = get_all()
    all_dict[username].update(container)

    for elmnt in all_dict.items():
        all_dict[elmnt[0]] = list(elmnt[1])


    file = open(filename, 'wt')
    json.dump(all_dict, file)
    file.close()

def add_usr(username):
    all_dict = get_all()
    all_dict.update({username:set()})

    for elmnt in all_dict.items():
        all_dict[elmnt[0]] = list(elmnt[1])

    file = open(filename, 'wt')
    json.dump(all_dict, file)
    file.close()