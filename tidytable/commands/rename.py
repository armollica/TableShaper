import pandas as pd
from tidytable.helpers import parse_key_value

def rename(df, way, expression):
    if way == 'map':
        df.columns = map(eval('lambda name: ' + expression), df.columns)
    elif way == 'assign':
        columns = dict()
        for chunk in expression.split(','):
            key_value = parse_key_value(chunk.strip())
            new_name = key_value['key'].strip()
            old_name = key_value['value'].strip()
            columns[old_name] = new_name
        df = df.rename(columns = columns)
    return df
