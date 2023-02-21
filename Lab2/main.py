import numbers
import listop


print("Hello world!")
do = str()
if do != 'numb' and do != 'list':
    do = input("Number operation(numb) or list(list) operation")

if do =='numb':
    numbers.do_numbers()
else:
    listop.do_list()