import click
import pandas as pd
from tidytable.util import generator

@click.command('input')
@click.option('-j', '--json', is_flag = True,
              help = 'Read as JSON instead of CSV')
@click.option('--json-format', default = 'records',
              type = click.Choice(['records', 'split', 'index', 'columns', 'values']),
              help = 'JSON string format.',
              show_default = True)
@click.argument('path', type = click.Path())
@generator
def cli(path, json, json_format):
    '''
    Read table.
    '''

    if path == '-':
        path_or_stream = click.get_text_stream('stdin')
    else:
        path_or_stream = path

    def read_df(path):
        if json:
            return pd.read_json(path_or_stream, orient = json_format)
        else:
            return pd.read_csv(path_or_stream)
    
    try:
        df = read_df(path)
        yield df
    except Exception as e:
        click.echo('Could not read CSV "%s": %s' % (filename, e), err = True)
