import click
import pandas as pd
from tidytable.helpers import processor
from tidytable.commands.choose import choose

@click.command('choose')
@click.option('-s', '--selection', 'way', flag_value = 'selection',
              default = True,
              help = 'Selection-based choosing')
@click.option('-f', '--filter', 'way', flag_value = 'filter',
              help = 'Filter-based choosing')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Subset columns.
    
    \b
    -f, --filter
    A python expression on each column name. If it evaluates to `True`
    then it's kept. The column name is loaded in as `name`.

    \b
    Examples:
    choose -f '"population" in name'

    \b
    -s, --selection (default)
    Provide a comma-separated list of column "selections".
    These can be single column names or sequential ranges of columns
    defined by the first and last column name of the sequence 
    separated by a colon. The tilde character (~) drops the selection,
    keeping all other columns.

    \b
    Examples:
    choose 'date, country, A, B, C, D'
    choose 'date, country, A:D'
    choose '~junk_column'
    choose '~junk_column_1:junk_column_20'
    '''
    for df in dfs:
        yield choose(df, way, expression)
