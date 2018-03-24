import click
import pandas as pd
from tableshaper import pick
from tableshaper.helpers import processor

@click.command('pick')
@click.option('-s', '--sift', 'way', flag_value = 'sift',
              help = 'Sift-based choosing')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Subset columns.
    
    \b
    Provide a comma-separated list of column "selections".
    These can be single column names or sequential ranges of columns
    defined by the first and last column name of the sequence 
    separated by a colon. The tilde character (~) drops the selection,
    keeping all other columns.

    \b
    Examples:
    pick 'date, country, A, B, C, D'
    pick 'date, country, A:D'
    pick '~junk_column'
    pick '~junk_column_1:junk_column_20'

    \b
    -s, --sift
    Change the column selection to sift-base mode.

    \b
    Provide a python expression on each column name. If it evaluates to
    `True` then it's kept. The column name is loaded in as `name`.

    \b
    Examples:
    pick -s '"population" in name'
    '''
    for df in dfs:
        if way == 'sift':
            column_list = filter(eval('lambda name: ' + expression), list(df))
            yield df[column_list]
        else:
            yield pick(expression)(df)