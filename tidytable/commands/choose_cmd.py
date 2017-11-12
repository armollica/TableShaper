import click
import pandas as pd
from tidytable.util import processor, selectify

@click.command('choose')
@click.option('-f', '--filter', 'filter_expression', type = click.STRING)
@click.option('-s', '--selection', 'selection_expression', type = click.STRING)
@processor
def cli(dfs, filter_expression, selection_expression):
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
    -s, --select
    Provide a comma-separated list of column "selections".

    \b
    Examples:
    choose -s 'date, country, A, B, C, D'
    choose -s 'date, country, A:D'
    choose -s '-junk_column'
    choose -s '-junk_column_1:junk_column_20'

    '''
    for df in dfs:
        if filter_expression is not None:
            column_list = filter(eval('lambda name: ' + filter_expression), list(df))
            df = df[column_list]
        if selection_expression is not None:
            column_list = selectify(list(df), selection_expression)
            df = df[column_list]
        yield df