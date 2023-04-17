def serialize(obj):
    default_types = [int, str, bool, dict, tuple, float, list, set, bool, type]
    if type(obj) in default_types:
        return '{' + basic_serailize(obj) +'}'

def basic_serailize(obj)->str:
    #int, float, string, dict, tuple, list, set, type, bool, function
    if isinstance(obj, int):
        return serialize_int(obj)
    elif isinstance(obj, float):
        return serialize_float(obj)
    elif isinstance(obj, str):
        return serialize_string(obj)
    elif isinstance(obj, dict):
        return serialize_dict(obj)
    elif isinstance(obj, bool):
        return serialize_bool(obj)
    elif isinstance(obj, list):
        return serialize_list(obj)
    elif isinstance(obj,set):
        return serialize_set(obj)
    elif isinstance(obj, tuple):
        serialize_tuple(obj)
        

basic:str = ' "type": "{type}", "type properties": {t_p}, "value": {val} '

def serialize_tuple(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ', '
    
    val = val[:-2] + ']'
    
    return basic.format(type="tuple", val=val, t_p='{}')

def serialize_set(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ', '
    
    val = val[:-2] + ']'
    
    return basic.format(type="set", val=val, t_p='{}')

def serialize_bool(obj)->str:
    return basic.format(type="bool", val=str(obj).lower(), t_p='{}') 

def serialize_int(obj)->str:
    return basic.format(type="int", val=str(obj), t_p='{}') 

def serialize_float(obj)->str:
    return basic.format(type="float", val=str(obj), t_p='{}')

def serialize_string(obj)->str:
    return basic.format(type="string", val='"'+obj+'"', t_p='{}')

def serialize_dict(obj:dict)->str:
    val = "["
    for it in obj.items():
        val += '{ "key": ' + serialize(it[0]) + ', "value": ' + serialize(it[1]) + '}, '
    
    val = val[:-2] + ']'
    return basic.format(type="dict", val=val, t_p='{}')

def serialize_list(obj):
    val = "["
    for it in obj:
        val += serialize(it) + ', '
    
    val = val[:-2] + ']'
    
    return basic.format(type="list", val=val, t_p='{}')    
