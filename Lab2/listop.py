import re

expr = r'\d+'
match_expr = r'(\d+\s*)+'

def do_list():
    
    numb_list = str()
    while not re.match(match_expr, numb_list):
        numb_list = input()

    numb_list = re.findall(expr, numb_list)
    numb_list = [int(n) for n in numb_list]
    numb_list = [ n for n in numb_list if n % 2 == 0]

    print(numb_list)