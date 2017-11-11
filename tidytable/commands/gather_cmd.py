import click
import pandas as pd
from tidytable.util import processor, selectify

@click.command('gather')
@click.option('-k', '--key', type = click.STRING, default = 'key',
              help = 'Column that will store columns names of gathered columns.')
@click.option('-v', '--value', type = click.STRING, default = 'value',
              help = 'Column that will store values of gathered column.s')
@click.argument('columns', type = click.STRING)
@processor
def cli(dfs, key, value, columns):
    '''
    Gather many columns into two key-value columns.
    '''
    for df in dfs:
        all_column_list = list(df)
        gather_column_list = selectify(list(df), columns)
        id_column_list = filter(lambda x: x not in gather_column_list, all_column_list)
        df = df.melt(id_vars = id_column_list,
                     value_vars = gather_column_list,
                     var_name = key,
                     value_name = value)
        yield df

