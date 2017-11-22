import click
import pandas as pd
from tidytable.util import processor

@click.command('join')
@click.option('-h', '--how',
              default = 'left',
              type = click.Choice(['left', 'right', 'outer', 'inner', 'bind-rows', 'bind-columns']),
              show_default = True)
@click.option('-k', '--keys', type = click.STRING)
@click.argument('other', default = '-', type = click.Path())
@processor
def cli(dfs, how, keys, other):
    '''
    Join tables.
    '''
    if other == '-':
        other_df = pd.read_csv(click.get_text_stream('stdin'))
    else:
        other_df = pd.read_csv(other)
    for df in dfs:
        if how == 'bind-rows':
            df = pd.concat([df, other_df])
        elif how == 'bind-columns':
            df = pd.concat([df, other_df], axis = 1)
        else:
            keys_list = map(lambda x: x.strip(), keys.split(','))
            df = df.merge(other_df, on = keys_list, how = how)
        yield df
