import click
import pandas as pd
from tidytable.util import processor

@click.command('output')
@click.option('-f', '--file', default='-', type=click.File('wb'),
              help = 'Filename for output CSV.',
              show_default = True)
@processor
def cli(dfs, file):
    '''
    Write table.
    '''
    try:
        for df in dfs:
            df.to_csv(file, index = False)
            yield df
    except Exception as e:
        click.echo('Could not write csv "%s": %s' %
                    (file, e), err = True)

