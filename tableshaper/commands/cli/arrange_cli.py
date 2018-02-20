import click
import pandas as pd
from tableshaper.helpers import processor
from tableshaper.commands.arrange import arrange

@click.command('arrange')
@click.argument('columns', type = click.STRING)
@processor
def cli(dfs, columns):
    '''
    Sort rows.
    
    Order is determined by values in a column (or columns).

    \b
    Examples:
    arrange 'mpg'
    arrange 'mpg:desc'
    arrange 'mpg, hp:desc'

    '''
    for df in dfs:
        yield arrange(df, columns)
