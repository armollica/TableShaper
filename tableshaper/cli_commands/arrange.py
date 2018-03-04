import click
from tableshaper import arrange
from tableshaper.helpers import processor

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
        column_list = map(lambda x: x.strip(), columns.split(','))
        yield arrange(*column_list)(df)
