def get_data(flag):
    if flag == "f":
        return fileread()
    elif flag == "m":
        return consoleread()


def fileread():
    file = None
    file_data = None

    try:
        file = open('/home/user/Documents/SCI/Lab1/Task 1/input.txt', 'rt')
        file_data = file.read()
        file.close()
    except OSError:
        print("Problem with a file")
        file_data = None
        

    return file_data


def consoleread():
    return input()
