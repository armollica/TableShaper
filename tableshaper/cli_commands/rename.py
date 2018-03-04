import click
from tableshaper.helpers import processor, parse_key_value

@click.command('rename')
@click.option('-m', '--map', 'way', flag_value = 'map',
              help = 'Map-based renaming')
@click.argument('expression', type = click.STRING)
@processor
def cli(dfs, way, expression):
    '''
    Rename columns.
    
    Provide a comma-separated list of column names assignment, i.e.: new <- old
    
    \b
    Example:
    rename 'id <- GEOID, fips <- state_fips'

    \b
    -m, --map
    Switch to the map-based renaming mode.

    Provide a python expression evaluated on each column name.
    The column name is loaded in as `name`.

    \b
    Example:
    rename -m 'name.upper()'
    rename -m 'name.strip().lower()'
    rename -m "'_'.join(name.split(' ')).strip().lower()"
    '''
    for df in dfs:
        if way == 'map':
            df.columns = map(eval('lambda name: ' + expression), df.columns)
            yield df
        else:
            columns = dict()
            for chunk in expression.split(','):
                key_value = parse_key_value(chunk.strip())
                new_name = key_value['key'].strip()
                old_name = key_value['value'].strip()
                columns[old_name] = new_name
            yield df.rename(columns = columns)
