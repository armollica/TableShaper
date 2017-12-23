import click
import pandas as pd
from tidytable.util import processor

@click.command('filter')
@click.option('-v', '--vectorized', 'way', flag_value = 'vectorized',
              default = True)
@click.option('-s', '--slice', 'way', flag_value = 'slice')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Subset rows. Kept rows are determined by a logical expression composed of
    column values.
    '''
    for df in dfs:
        if way == 'slice':
            [start, end] = map(lambda x: int(x.strip()), expression.split(':'))
            df = df.iloc[start:end]
        elif way == 'vectorized':
            df = df[eval(expression, df.to_dict('series'))]
        yield df
