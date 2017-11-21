import click
import pandas as pd
from tidytable.util import processor

@click.command('filter')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, expression):
    '''
    Subset rows. Kept rows are determined by a logical expression composed of
    column values.
    '''
    for df in dfs:
        df = df[eval(expression, df.to_dict('series'))]
        yield df
