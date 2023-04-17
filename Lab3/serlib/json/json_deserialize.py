import re

def parse_bracket(txt:str, isFigure)->tuple[str, int]:
    reg = ""
    
    if isFigure is True:
        reg = r'{}'
    else:
        reg = r'[]'
    
    count = 0
    
    for ch in txt:
        if
    
    
    
    

def parse_value(txt:str)->tuple[str, int]:
    first_symb = re.search(r'[^\s:]', txt)
    val:str = ""
    if first_symb.string == '"':
        val = re.search(r'"(?:[^"]|(?<=\\)")*"', txt).string
    elif first_symb.string == '[':
        pass
    elif first_symb.string == '{':
        # reg = r'{(?<InsadeBrackets>[^{}]*(({(?<Open>)[^{}]*)+(}(?<-Open>)[^{}]*)+)*(?(Open)(?!)))}'
        val = re.search(reg, txt).string
    
    return val
    
    
    
def parse_to_kv(txt:str)->dict:
    d = {}
    while txt != '':
        key_match = re.search(r'"[^"]*"', txt)
        txt = txt[key_match.span()[1]::]
        val = parse_value(txt)
        
        
        
        

def deserialize(txt:str):
    basic_types = {"str", "dict", "tuple", 
                   "function", "bool", "set",
                   "int", "float", "type", "list"
                   }
    typesearch = r'"type":"([^"])"'
    typ = re.findall(typesearch, txt)[0]
    if type in basic_types:
        basic_deserialize(txt, typ)
    
def basic_deserialize(txt:str, typ):
    if typ == "string":
        
    