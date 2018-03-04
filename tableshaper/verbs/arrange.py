def arrange(*names):
    by = []
    ascending = []

    for name in names:
        is_ascending = True
        if name.endswith(':desc'):
            is_ascending = False
            name = name[:-5]
        by.append(name)
        ascending.append(is_ascending)
    
    return lambda df: df.sort_values(by = by, ascending = ascending)
