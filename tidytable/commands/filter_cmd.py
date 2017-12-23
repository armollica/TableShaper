import click
import pandas as pd
from tidytable.util import processor

@click.command('filter')
@click.option('-v', '--vectorized', 'way', flag_value = 'vectorized',
              default = True,
              help = 'Vectorized filtering')
@click.option('-s', '--slice', 'way', flag_value = 'slice',
              help = 'Slice-based filtering')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Subset rows.
    
    Rows are kept based on a logical expression (true/false) or by a range of
    row indices.

    \b
    -v, --vectorized (default)
    Rows are kept based on a python expression that evaluates to true or false.
    The columns of the table are put into the namespace a pandas series.

    \b
    Examples:
    filter 'population > 1000'
    filter 'state == "55"'
    filter 'state.isin(["55", "56"])'

    \b
    -s, --slice
    Specify a range of indices following this format: start:end

    \b
    Examples:
    filter -s 1:5
    filter -s 25:75
    '''
    for df in dfs:
        if way == 'slice':
            [start, end] = map(lambda x: int(x.strip()), expression.split(':'))
            df = df.iloc[start:end]
        elif way == 'vectorized':
            df = df[eval(expression, df.to_dict('series'))]
        yield df
