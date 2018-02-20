import click
import pandas as pd
from tableshaper.helpers import processor, parse_key_value

def rename(df, way, expression):
    if way == 'map':
        df.columns = map(eval('lambda name: ' + expression), df.columns)
    elif way == 'assign':
        columns = dict()
        for chunk in expression.split(','):
            key_value = parse_key_value(chunk.strip())
            new_name = key_value['key'].strip()
            old_name = key_value['value'].strip()
            columns[old_name] = new_name
        df = df.rename(columns = columns)
    return df

@click.command('rename')
@click.option('-a', '--assign', 'way', flag_value = 'assign', default = True,
              help = 'assign-based renaming (default)')
@click.option('-m', '--map', 'way', flag_value = 'map',
              help = 'map-based renaming')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Rename columns.
    
    \b
    -a, --assign (default)
    A comma-separated list of column names assignment, i.e.: new <- old
    
    \b
    Example:
    rename 'id <- GEOID, fips <- state_fips'

    \b
    -m, --map
    A python expression evaluated on each column name.
    The column name is loaded in as `name`.

    \b
    Example:
    rename -m 'name.upper()'
    rename -m 'name.strip().lower()'
    rename -m "'_'.join(name.split(' ')).strip().lower()"
    '''
    for df in dfs:
        yield rename(df, way, expression)
