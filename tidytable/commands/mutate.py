import pandas as pd
from tidytable.helpers import processor, parse_key_value

def row_mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: x.apply(lambda y: eval(expression, y.to_dict()), axis = 1)})

def column_mutate(df, column_name, expression):
    return df.assign(**{ column_name: lambda x: eval(expression, x.to_dict('series')) })

def column_mutate_grouped(df, groups, column_name, expression):
    def apply_func(df):
        return column_mutate(df, column_name, expression)
    return df.groupby(groups).apply(apply_func).reset_index(drop = True)

def mutate(df, way, group_by, mutation):
    key_value = parse_key_value(mutation.strip())
    name = key_value['key']
    expression = key_value['value']
    if way == 'row-wise':
        df = row_mutate(df, name, expression)
    elif way == 'vectorized':    
        if group_by is not None:     
            groups = map(lambda x: x.strip(), group_by.split(','))
            df = column_mutate_grouped(df, groups, name, expression)
        else:
            df = column_mutate(df, name, expression)
    return df
