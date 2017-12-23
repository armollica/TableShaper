import click
import pandas as pd
from tidytable.util import processor

@click.command('arrange')
@click.argument('columns', type = click.STRING)
@processor
def cli(dfs, columns):
    '''
    Sort rows.
    
    Order is determined by values in a column (or columns).

    \b
    Examples:
    arrange 'mpg'
    arrange 'mpg:desc'
    arrange 'mpg, hp:desc'

    '''
    column_list = []
    ascending_list = []
    for column in columns.split(','):
        column = column.strip()
        ascending = True
        if column.endswith(':desc'):
            ascending = False
            column = column[:-5]
        column_list.append(column)
        ascending_list.append(ascending)
    for df in dfs:
        df = df.sort_values(by = column_list, ascending = ascending_list)
        yield df
