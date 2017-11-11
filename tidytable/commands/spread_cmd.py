import click
import pandas as pd
from tidytable.util import processor

def spread(df, key, value):
    indexes = list(df.columns.drop(value))
    df = df.set_index(indexes).unstack(key).reset_index()
    df.columns = [i[1] if i[0] == value else i[0] for i in df.columns]
    return df

@click.command('spread')
@click.option('-k', '--key', type = click.STRING, required = True,
              help = 'Column that stores columns names to be spread.')
@click.option('-v', '--value', type = click.STRING, required = True,
              help = 'Column that stores values to be spread.')
@processor
def cli(dfs, key, value):
    '''
    Spread two key-value columns to multiple columns.
    '''
    for df in dfs:
        df = spread(df, key, value)
        yield df
