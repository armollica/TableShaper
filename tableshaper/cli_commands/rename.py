import click
from tableshaper.helpers import parse_key_value

@click.command('rename')
@click.option('-m', '--map', 'way', flag_value = 'map',
              help = 'Map-based renaming')
@click.argument('expression', type = click.STRING)
@click.pass_context
def cli(context, way, expression):
    '''
    Rename columns.
    
    Provide a comma-separated list of column names assignment that follow
    this format:

    new = old

    Where the "old" column name is changed to whatever "new" is.
    
    \b
    Example:
    rename 'id = GEOID, fips = state_fips'

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
    table = context.obj['get_target']()

    if way == 'map':
        table.columns = map(eval('lambda name: ' + expression), table.columns)
    else:
        columns = dict()
        for chunk in expression.split(','):
            key_value = parse_key_value(chunk.strip())
            new_name = key_value['key'].strip()
            old_name = key_value['value'].strip()
            columns[old_name] = new_name
        table = table.rename(columns = columns)
    
    context.obj['update_target'](table)
