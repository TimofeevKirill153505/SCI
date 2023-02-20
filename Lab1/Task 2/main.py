import json

import users_com as u_c
import commands as com



data:dict = None
try:
    data = json.load("data.txt")
except OSError:
    print("Cannot open data file")
    quit()


ex:bool = False
while not ex:
    username = u_c.authorize()
    if username == False: quit()
    if com.do_commands(username) == False: quit()