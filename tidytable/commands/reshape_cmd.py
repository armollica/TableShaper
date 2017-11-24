

import click
import pandas as pd
from tidytable.util import processor, selectify

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

@click.command('reshape')
@click.option('-w', '--way',
              default = 'gather',
              type = click.Choice(['gather', 'spread']),
              show_default = True)
@click.option('-k', '--key', type = click.STRING, default = 'key',
              help = 'Key column')
@click.option('-v', '--value', type = click.STRING, default = 'value',
              help = 'Value column')
@click.option('-c', '--columns', type = click.STRING, help = 'Selection of columns to be gathered')
@processor
def cli(dfs, way, key, value, columns):
    '''
    Reshape table. Gather many columns into two key-value columns. Or Spread
    two key-value columns to multiple columns.
    '''
    for df in dfs:    
        if way == 'gather':
            df = gather(df, key, value, columns)
        elif way == 'spread':
            df = spread(df, key, value)    
        yield df
