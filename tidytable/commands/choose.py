import pandas as pd
from tidytable.helpers import processor, selectify

def choose(df, way, expression):
    if way == 'filter':
        column_list = filter(eval('lambda name: ' + expression), list(df))
        df = df[column_list]
    elif way == 'selection':
        column_list = selectify(list(df), expression)
        df = df[column_list]
    return df
