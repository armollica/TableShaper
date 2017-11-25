import click
import pandas as pd
from tidytable.util import processor

@click.command('rename')
@click.option('-w', '--way',
              default = 'assign',
              type = click.Choice(['assign', 'map']),
              show_default = True)
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Rename columns.
    
    \b
    --way assign (default)
    A comma-separated list of column names assignment, i.e.: new <- old
    
    \b
    Example:
    rename 'id <- GEOID, fips <- state_fips'

    \b
    --way map
    A python expression evaluated on each column name.
    The column name is loaded in as `name`.

    \b
    Example:
    rename --way map 'name.strip().lower()'
    rename -w map "'_'.join(name.split(' ')).strip().lower()"

    '''
    for df in dfs:
        if way == 'map':
            df.columns = map(eval('lambda name: ' + expression), df.columns)
        elif way == 'assign':
            columns = dict()
            for chunk in expression.split(','):
                names = chunk.split('<-')
                columns[names[1].strip()] = names[0].strip()
            df = df.rename(columns = columns)
        yield df
