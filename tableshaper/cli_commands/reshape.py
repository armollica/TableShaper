import click
from tableshaper import gather, spread
from tableshaper.helpers import selectify

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
@click.pass_context
def cli(context, way, key, value, columns):
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
    table = context.obj['get_target']()

    if way == 'gather':
        table = gather(key, value, columns)(table)
    elif way == 'spread':
        table = spread(key, value)(table)
    
    context.obj['update_target'](table)
