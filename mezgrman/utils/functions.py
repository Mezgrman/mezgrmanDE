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

def multiline_join(blocks, separator = ""):
    lines = []
    n = 0
    for block in blocks:
        block_lines = block.splitlines()
        for i in range(len(block_lines)):
            try:
                lines[i] += block_lines[i]
            except IndexError:
                lines.append(block_lines[i])
            if(n < len(blocks) - 1):
                lines[i] += separator
        n += 1
    result = "\n".join(lines)
    return result