import json

file:str = "data.txt"

def get_all()->dict:
    return json.load(file)

def get_users():
    return json.load(file).keys()

def get_set(username:str):
    return json.load(file)[username]

def save_container(username:str, container:set):
    all_dict:dict = get_all()
    all_dict[username].update(container)
    json.dump(all_dict)
    