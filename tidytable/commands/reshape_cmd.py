import click
import pandas as pd
from tidytable.util import processor
from tidytable.operations import gather, spread

@click.command('reshape')
@click.option('-g', '--gather', 'way', flag_value = 'gather', default = True,
              help = 'Go from wide to long (default)')
@click.option('-s', '--spread', 'way', flag_value = 'spread',
              help = 'Go from long to wide')
@click.option('-k', '--key', type = click.STRING, default = 'key',
              help = 'Key column')
@click.option('-v', '--value', type = click.STRING, default = 'value',
              help = 'Value column')
@click.option('-c', '--columns', type = click.STRING, help = 'Selection of columns to be gathered')
@processor
def cli(dfs, way, key, value, columns):
    '''
    Reshape table.

    \b
    -g, --gather (default)
    Go from wide to long. Gather many columns into two key-value columns.

    \b
    Examples:
    reshape -k year -v population -c 1995:2013 \
    
    \b
    -s, --spread
    Go from long to wide. Spread two key-value columns to multiple columns.

    \b
    Examples:
    reshape -s -k year -v population
    '''
    for df in dfs:    
        if way == 'gather':
            df = gather(df, key, value, columns)
        elif way == 'spread':
            df = spread(df, key, value)    
        yield df
