import click
import pandas as pd
from tt.util import processor, selectify

@click.command('choose')
@click.argument('columns', type = click.STRING)
@processor
def cli(dfs, columns):
    '''
    Subset columns. Provide a comma-separated list of column names.
    '''
    for df in dfs:
        column_list = selectify(list(df), columns)
        df = df[column_list]
        yield df