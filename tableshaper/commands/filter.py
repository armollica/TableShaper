import click
import pandas as pd
from tableshaper.helpers import processor

def filter_dataframe(df, way, expression):
    if way == 'slice':
        [start, end] = map(lambda x: int(x.strip()), expression.split(':'))
        start = start - 1  # one-based index
        df = df.iloc[start:end]
    elif way == 'vectorized':
        df = df[eval(expression, df.to_dict('series'))]
    return df

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
    Specify a range of indices following this format: start:end.
    It's a one-based index; the first row starts at one, not zero. Indexes are
    inclusive. The start row, the end row and all rows in-between will be
    included.
    
    \b
    Examples:
    filter -s 1:5
    filter -s 25:75
    '''
    for df in dfs:
        yield filter_dataframe(df, way, expression)
