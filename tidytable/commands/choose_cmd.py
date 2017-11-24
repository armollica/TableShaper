import click
import pandas as pd
from tidytable.util import processor, selectify

@click.command('choose')
@click.option('-w', '--way',
              default = 'selection',
              type = click.Choice(['selection', 'filter']),
              show_default = True)
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Subset columns.
    
    \b
    -k, --keep
    A python expression on each column name. If it evaluates to `True`
    then it's kept. The column name is loaded in as `name`.

    \b
    Examples:
    choose -f '"population" in name'

    \b
    -c, --columns
    Provide a comma-separated list of column "selections".
    These can be single column names or sequential ranges of columns
    defined by the first and last column name of the sequence 
    separated by a colon. The tilde character (~) drops the selection.

    \b
    Examples:
    choose -s 'date, country, A, B, C, D'
    choose -s 'date, country, A:D'
    choose -s '~junk_column'
    choose -s '~junk_column_1:junk_column_20'
    '''
    for df in dfs:
        if way == 'filter':
            column_list = filter(eval('lambda name: ' + expression), list(df))
            df = df[column_list]
        if way == 'selection':
            column_list = selectify(list(df), expression)
            df = df[column_list]
        yield df