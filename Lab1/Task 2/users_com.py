import file_module as f_m

def authorize():
    usrs = f_m.get_users()
    if usrs == False: return False

    while True:
        username:str = input("Enter username\n")
        
        if username == ":q":
            return False

        if username == ":c":
            username = create_user(usrs)
            return username

        if username in usrs:
           return username
        
        print("There is no user named ", username, ". Type :c if you want to create a new one.")

def create_user(usrs:set):
    while True:
        new_usr = input("Enter your name\n")

        if new_usr == ":q": return False

        if not new_usr in usrs:
            f_m.add_usr(new_usr)
            return new_usr
        print("There is a user with name ", new_usr, ". Please, try again")