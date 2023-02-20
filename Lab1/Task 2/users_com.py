import file_module as f_m

def authorize():
    while True:
        username:str = input("Enter username\n")
        
        if username == ":q":
            return False

        if username in f_m.get_users():
           return username
        
        print("There is no user named " + username)