def view_tuple(obj):
    """
    Parse a variable and return a tuple for reverse URL lookup
    """
    
    if type(obj) is str:
        return (obj, (), {})

    if len(obj) == 3:
        return obj
    
    types = tuple(map(type, obj))
    
    if types == (str, tuple):
        return (obj[0], obj[1], {})
    
    if types == (str, dict):
        return (obj[0], (), obj[1])
    
    return ('', (), {})