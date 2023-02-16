from inputmodule import get_data

input_type = input("Do you want input text by file(f) or by console message(m)" + "\n")

if input_type != "m" and input_type != "f": 
    print("Error in input")
    quit()

data = get_data(input_type)

print(data)