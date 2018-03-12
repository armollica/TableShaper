import click
from tableshaper import sort
from tableshaper.helpers import processor

@click.command('sort')
@click.argument('columns', type = click.STRING)
@processor
def cli(dfs, columns):
    '''
    Sort rows.
    
    Order is determined by values in a column (or columns).

    \b
    Examples:
    sort 'mpg'
    sort 'mpg:desc'
    sort 'mpg, hp:desc'

    '''
    for df in dfs:
        column_list = map(lambda x: x.strip(), columns.split(','))
        yield sort(*column_list)(df)
