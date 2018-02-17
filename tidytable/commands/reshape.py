import click
import pandas as pd
from tidytable.helpers import selectify

def gather(df, key, value, columns):
    all_column_list = list(df)
    gather_column_list = selectify(list(df), columns)
    id_column_list = filter(lambda x: x not in gather_column_list, all_column_list)
    return df.melt(id_vars = id_column_list,
                   value_vars = gather_column_list,
                   var_name = key,
                   value_name = value)

def spread(df, key, value):
    indexes = list(df.columns.drop(value))
    df = df.set_index(indexes).unstack(key).reset_index()
    df.columns = [i[1] if i[0] == value else i[0] for i in df.columns]
    return df

def reshape(df, way, key, value, columns):
    if way == 'gather':
        df = gather(df, key, value, columns)
    elif way == 'spread':
        df = spread(df, key, value)    
    return df
