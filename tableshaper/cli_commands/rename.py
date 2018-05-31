import inflection, click
from tableshaper.helpers import parse_key_value

def snake_case(x):
    return inflection.underscore(inflection.parameterize(unicode(x.lower())))

def kebab_case(x):
    return inflection.dasherize(snake_case(x))

def camel_case(x):
    return inflection.camelize(snake_case(x), uppercase_first_letter=False)

def sentence_case(x):
    return inflection.humanize(snake_case(x))

def title_case(x):
    return inflection.titleize(snake_case(x))

@click.command('rename')
@click.option('-m', '--map', 'way', flag_value = 'map',
              help = 'Map-based renaming')
@click.option('-s', '--sanitize', 'way', flag_value = 'sanitize',
              help = 'Santize names. One of: snake, camel, kebab, sentence, title')
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

    \b
    -s, --sanitize
    "Sanitize" all column names using one of the following transforms:
    * camel    -> camelCase
    * snake    -> snake_case
    * kebab    -> kebab-case
    * sentence -> Sentence case
    * title    -> Title Case

    \b
    Example:
    rename -s snake
    rename -s title
    '''
    table = context.obj['get_target']()

    if way == 'map':
        table.columns = map(eval('lambda name: ' + expression), table.columns)
    elif way == 'sanitize':
        if expression == 'camel':
            table.columns = map(camel_case, table.columns)
        elif expression == 'snake':
            table.columns = map(snake_case, table.columns)
        elif expression == 'kebab':
            table.columns = map(kebab_case, table.columns)
        elif expression == 'sentence':
            table.columns = map(sentence_case, table.columns)
        elif expression == 'title':
            table.columns = map(title_case, table.columns)
        else:
            click.echo('"{}" isn\'t a valid sanitize option. Must be one of camelCase, snake_case, kebab-case or Humanized.'.format(expression), err=True)
    else:
        columns = dict()
        for chunk in expression.split(','):
            key_value = parse_key_value(chunk.strip())
            new_name = key_value['key'].strip()
            old_name = key_value['value'].strip()
            columns[old_name] = new_name
        table = table.rename(columns = columns)
    
    context.obj['update_target'](table)
