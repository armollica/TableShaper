import click
from tableshaper import sift
from tableshaper.helpers import processor

@click.command('sift')
@click.option('-s', '--slice', 'way', flag_value = 'slice',
              help = 'Slice-based filtering')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Subset rows.
    
    Rows are kept based on a logical expression (true/false) or by a range of
    row indices.

    The default behavior is to keep rows based on a python expression that
    evaluates to true or false. The columns of the table are put into the
    namespace as a pandas series.

    \b
    Examples:
    sift 'population > 1000'
    sift 'state == "55"'
    sift 'state.isin(["55", "56"])'

    \b
    -s, --slice
    Change to the slice-based mode.

    Specify a range of indices following this format: start:end.
    It's a one-based index; the first row starts at one, not zero. Indexes are
    inclusive. The start row, the end row and all rows in-between will be
    included.
    
    \b
    Examples:
    sift -s 1:5
    sift -s 25:75
    '''
    for df in dfs:
        if way == 'slice':
            [start, end] = map(lambda x: int(x.strip()), expression.split(':'))
            start = start - 1  # one-based index
            yield df.iloc[start:end]
        else:
            yield sift(expression)(df)
