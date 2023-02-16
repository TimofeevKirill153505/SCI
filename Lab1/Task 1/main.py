from input_module import get_text

import text_analysis as t_a

input_type = input("Do you want input text by file(f) or by console message(m)" + "\n")

if input_type != "m" and input_type != "f": 
    print("Error in input")
    quit()

text = get_text(input_type)

if text == None: quit()

N = int(input("Input N for N-gram search\n"))
K = int(input("Input K for N-gram search\n"))

result = t_a.analyze_text(text, N, K)

print(result)