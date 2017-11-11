import click
import pandas as pd
from tt.util import processor

@click.command('filter')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, expression):
    '''
    Subset rows. Kept rows are determined by a logical expression composed of
    column values.
    '''
    for df in dfs:
        df.query(expression, inplace = True)
        yield df
