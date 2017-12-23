import click
import pandas as pd
from tidytable.util import processor

@click.command('join')
@click.option('-l', '--left', 'way', flag_value = 'left', default = True)
@click.option('-r', '--right', 'way', flag_value = 'right')
@click.option('-o', '--outer', 'way', flag_value = 'outer')
@click.option('-i', '--inner', 'way', flag_value = 'inner')
@click.option('-r', '--bind-rows', 'way', flag_value = 'bind-rows')
@click.option('-c', '--bind-columns', 'way', flag_value = 'bind-columns')
@click.option('-k', '--keys', type = click.STRING)
@click.argument('other', default = '-', type = click.Path())
@processor
def cli(dfs, way, keys, other):
    '''
    Join tables.
    '''
    if other == '-':
        other_df = pd.read_csv(click.get_text_stream('stdin'))
    else:
        other_df = pd.read_csv(other)
    for df in dfs:
        if way == 'bind-rows':
            df = pd.concat([df, other_df])
        elif way == 'bind-columns':
            df = pd.concat([df, other_df], axis = 1)
        else:
            keys_list = map(lambda x: x.strip(), keys.split(','))
            df = df.merge(other_df, on = keys_list, how = way)
        yield df
