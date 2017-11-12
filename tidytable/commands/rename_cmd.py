import click
import pandas as pd
from tidytable.util import processor

@click.command('rename')
@click.option('-m', '--map', 'map_expression', type = click.STRING)
@click.option('-a', '--assign', type = click.STRING)
@processor
def cli(dfs, assign, map_expression):
    '''
    Rename columns.
    
    \b
    -a, --assign: 
    A comma-separated list of column names assignment, i.e.: new <- old
    
    \b
    Example:
    rename -a 'id <- GEOID, fips <- state_fips'

    \b
    -m, --map:
    A python expression evaluated on each column name.
    The column name is loaded in as `name`.

    \b
    Example:
    rename -m 'name.strip().lower()'
    rename -m "'_'.join(name.split(' ')).strip().lower()"

    '''
    for df in dfs:
        if map_expression is not None:
            df.columns = map(eval('lambda name: ' + map_expression), df.columns)
        if assign is not None:
            columns = dict()
            for chunk in assign.split(','):
                names = chunk.split('<-')
                columns[names[1].strip()] = names[0].strip()
            df = df.rename(columns = columns)
        yield df
