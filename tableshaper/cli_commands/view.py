import click
import pandas as pd
from tableshaper.helpers import processor

@click.command('view')
@click.option('-n', '--top', type = int,
              help = 'Display top `n` rows')
@click.option('-i', '--info', 'way', flag_value = 'info',
              help = 'Display info on a table')
@click.option('-s', '--stats', 'way', flag_value = 'stats',
              help = 'Display summary stats on the columns')
@processor
def cli(dfs, top, way):
    '''
    View table.

    Display table in a human-readable format. Or print summary information
    about the table.

    Calling `view` by itself will print the first and last 30 rows of the table.

    \b
    -n, --top
    Display the top `n` rows of the table.

    \b
    Example:
    view -n 5  # show the top 5 rows

    \b
    -i, --info
    Display a summary of the table. This includes the number of rows and
    columns, each column's name, its data type and the number of non-null
    values it has. Also displays the memory usage of the table.

    \b
    -s, --stats
    Display summary statistics on columns in the table.
    
    For numbers this will includes the count, mean, standard deviation, minimum,
    maximum, 25th percentile, median and 75th percentile.

    For strings and timestamps it will include the count, the number of unique
    values, the most common value and the number of times it occurs.
    Timestamps also include the first and last items.
    '''
    for df in dfs:
        if (top is not None):
            print df.head(top)
        else:
            if (way == 'info'):
                df.info(verbose = True, null_counts = True)
            elif (way == 'stats'):
                with pd.option_context('display.max_rows', None):
                    print df.describe(include = 'all').transpose()
            else:
                print df
        raise StopIteration
